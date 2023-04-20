

from django.shortcuts import render, redirect

from common.util.functions import event_id
from conversion_tracking.tasks import conversion_tracking
from session_management.models import Category
from session_management.views import _session
from blog.models import BlogPage
import stripe
from quiz_site.settings import STRIPE_SECRET_KEY
from django.contrib import messages
from quizPayments.models import Order

from quizConversionTracking.tasks import  conversion_tracking_user_quiz

stripe.api_key = STRIPE_SECRET_KEY

def home(request):

    context = {
    }


    purchase_event_unique_id = event_id()
    vc_event_unique_id = event_id()

    context['pv_event_unique_id'] = purchase_event_unique_id
    context['vc_event_unique_id'] = vc_event_unique_id


    event_source_url = request.META.get('HTTP_REFERER')
    session = _session(request)
    category = Category.objects.all()[0]

    try:
        # Need to fix this to ensure different ids
        conversion_tracking.delay(event_name="PageView", event_id=purchase_event_unique_id, event_source_url=event_source_url, category_id=category.id, session_id=session.session_id)  
        conversion_tracking.delay(event_name="ViewContent", event_id=vc_event_unique_id, event_source_url=event_source_url, category_id=category.id, session_id=session.session_id)  

        print("tracking conversion")
    except Exception as e:
        print("failed conv tracking")
        print(e)


    if request.GET.get('payment_intent', None):
        
        payment_intent = stripe.PaymentIntent.retrieve(
        request.GET.get('payment_intent'),
        )   

        print(payment_intent) 
        if payment_intent['status'] == "succeeded":
            order = Order.objects.get(payment_intent_id=request.GET.get('payment_intent'))
            order.is_paid = True
            order.save()


            messages.success(request, f"Order placed, you should receive an email with your order details soon! Your order number is {order.number}.")
    
    
    
    
            print("TAKE UQUIZ")
            
            purchase_event_unique_id = event_id()

            event_source_url = request.META.get('HTTP_REFERER')

            session = _session(request)

            quiz_id = order.response.quiz.id

            try:
                # Need to fix this to ensure different ids
                conversion_tracking_user_quiz.delay(event_name="Purchase", event_id=purchase_event_unique_id, event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)  

                print("tracking conversionuser quiz purchase")
            except Exception as e:
                print("failed conv tracking purchase event quiz")
                print(e)

    
    
    
    
    
    
    
    return render(request, 'home_site2/index.html', context=context)



def robots_txt(request):
    return render(request, 'robots.txt')

# def about(request):
#     return render(request, 'home_site2/pages/about.html')

# def contact(request):
#     return render(request, 'home_site2/pages/contact.html')

def tandc(request):
    return render(request, 'home_site2/pages/tandc.html')


def privpolicy(request):
    context = {
    }
    return render(request, 'home_site2/pages/privpolicy.html', context=context)

def deliveryinfo(request):
    return render(request, 'home_site2/pages/deliveryinfo.html')


def refundpolicy(request):
    return render(request, 'home_site2/pages/refundpolicy.html')

def pricing(request):
    return render(request, 'home_site2/pages/pricing.html')


def redirect_old_blog(request, slug):
    page = BlogPage.objects.get(slug=slug)
    
    return redirect(page.get_full_url(request=request))
