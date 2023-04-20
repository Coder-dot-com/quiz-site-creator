from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from .forms import ProductCreateForm
from .models import Product, ProductImage, Order
from uuid import uuid4
import os
import datetime
import stripe
from common.util.functions import event_id
from quiz_site.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from quizRender.models import Response

stripe.api_key = STRIPE_SECRET_KEY
stripe_pub_key = STRIPE_PUBLIC_KEY

@login_required
def add_stripe_integration(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)
    context = {
        'user_quiz': user_quiz
    }

    user_quiz.stripe_public_key = request.POST['stripe_public_key']

    user_quiz.stripe_secret_key = request.POST['stripe_secret_key']

    user_quiz.save()

    return render(request, 'quiz_payments/payment_settings.html', context=context)


@login_required
def delete_stripe_integration(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)
    context = {
        'user_quiz': user_quiz
    }

    user_quiz.stripe_public_key = None
    user_quiz.stripe_secret_key = None

    user_quiz.save()

    return render(request, 'quiz_payments/payment_settings.html', context=context)


@login_required
def add_image_quiz_product(request, quiz_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        product = Product.objects.get(quiz=user_quiz)

        if request.method == 'POST':
            images = request.FILES.getlist('image')

            for image in images:
                if image.size < 20000000:
                    file_name = image.name
                    file_ext = os.path.splitext(file_name)[1]
                    if file_ext == '.jpeg':
                        file_ext = '.jpg'

                    image.name = f"{uuid4()}{file_ext}"
                    ProductImage.objects.create(image=image, product=product)

                else:
                    return HttpResponse("Image too big, refresh too try again, max size 20mb")
    context = {
        'user_quiz': user_quiz,
        'product': product,

    }

    return render(request, 'quiz_payments/add_product_image.html', context=context)


@login_required
def delete_image_quiz_product(request, quiz_id, image_id):
    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        product = Product.objects.get(quiz=user_quiz)
        ProductImage.objects.get(product=product, id=image_id).delete()

    context = {
        'user_quiz': user_quiz,
        'product': product,

    }

    return render(request, 'quiz_payments/add_product_image.html', context=context)




def post_shipping_address_form(request, quiz_id, response_id):
    user_quiz = UserQuiz.objects.filter(id=quiz_id)
    if user_quiz.exists():
        user_quiz = user_quiz[0]
        product = Product.objects.get(quiz=user_quiz)
        response = Response.objects.get(response_id=response_id)
        print(request.POST)
        order = Order()

        order.response = response

        order.first_name = request.POST['first_name']
        order.last_name = request.POST['last_name']
        order.shipping_email = request.POST['shipping_email']
        order.address_line_1 = request.POST['address_line_1']
        order.address_line_2 = request.POST['address_line_1']
        order.country = request.POST['country']
        order.city = request.POST['city']
        order.zip_postcode = request.POST['zip_postcode']

        order.product = product
        order.total =  product.price
        order.currency_code = product.currency.currency_code

        order.save()

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")

        order_number = str(current_date) + str(order.id)
        order.number = order_number

        order.save()

        #create strip payment intent and rendr stri[e]
        intent = stripe.PaymentIntent.create(
            amount=int(order.total*100),
            currency=order.currency_code,
            payment_method_types=[
                "card",
            ],
            metadata={
            'email': order.shipping_email,
        },
        )

        client_secret = intent.client_secret
        payment_intent_id = intent.id

        order.payment_intent_id = payment_intent_id
        order.save()


        return_url = request.build_absolute_uri(reverse('home'))

        context = {
            'user_quiz': user_quiz,
            'product': product,
            'client_secret': client_secret,
            'stripe_pub_key': stripe_pub_key,
            'return_url': return_url,
            'order': order,
            'response_id': response_id,


        }

        return render(request, 'quiz_payments/payment_form.html', context=context)