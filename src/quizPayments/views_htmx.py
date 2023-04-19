from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from django.shortcuts import render, HttpResponse
from .forms import ProductCreateForm
from .models import Product, ProductImage
from uuid import uuid4
import os


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
