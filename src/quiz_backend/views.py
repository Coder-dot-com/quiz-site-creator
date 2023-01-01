from django.shortcuts import render

# from quiz_backend.models import QuizOrder
from emails.tasks import quiz_order_confirmed
from conversion_tracking.tasks import conversion_tracking
from session_management.models import Category
from quiz_site.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from session_management.views import _session
from django.shortcuts import HttpResponse
from .models import QuizOrder
import stripe
# Create your views here.

stripe.api_key = STRIPE_SECRET_KEY

stripe_pub_key = STRIPE_PUBLIC_KEY

def _post_quiz_payment_success(payment_intent):
    #Use the stripe payment intent to call the api and verify
    paid = None
    if payment_intent:
        #Use payment intent to check if payment was successful, get list of charges
        intent = stripe.PaymentIntent.retrieve(payment_intent)
        charges = intent.charges.data
        for charge in charges:
            if (charge['paid']) == True:
                paid = True
    
    if paid:
        order = QuizOrder.objects.get(payment_intent_id=payment_intent)
        order.status = "paid"
        order.save()
        order.response.purchased = True
        order.response.save()
        
        #create task and Delay basic text email

        quiz_order_confirmed.delay(payment_intent)

        #Conv tracking

        category = Category.objects.all()[0]
        conversion_tracking.delay(event_name="Purchase", event_id=order.order_number, category_id=category.id, session_id=order.session.session_id)  


def quiz_payment_success(request):
    # Post success stuff...
    payment_intent_id = (request.GET['payment_intent'])
    session = _session(request)

    #get order with bmatching intent and session
    try:
        order = QuizOrder.objects.get(payment_intent_id=payment_intent_id, session=session)
        _post_quiz_payment_success(payment_intent_id)
        context = {'order': order,}
        #Pixel unique id is from order number
        return render(request, 'quiz_backend/thankyou.html', context=context)
    except QuizOrder.DoesNotExist:
        return HttpResponse(500)