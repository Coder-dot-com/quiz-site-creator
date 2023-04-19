from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from django.shortcuts import render
from .forms import ProductCreateForm
from .models import Product

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
def get_create_product_form(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    context = {
        'user_quiz': user_quiz,
 
    }

    product = None

    try:
        product = Product.objects.get(quiz=user_quiz)
        context['form'] = ProductCreateForm(instance=product),
        context['product'] = product,       
    except Product.DoesNotExist:
        context['form'] = ProductCreateForm(),

        pass


 
    return render(request, 'quiz_payments/create_product.html', context=context)

@login_required
def create_product(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    product = None

    try:
        product = Product.objects.get(quiz=user_quiz)
    except Product.DoesNotExist:
        pass

    if product:
        form = ProductCreateForm(request.POST, instance=product).save()

    else:
        form = ProductCreateForm(request.POST).save(commit=False)
        form.quiz = user_quiz
        form.save()



    context = {
        'user_quiz': user_quiz,
        'form': form,
        'product': product,
    }


 
    return render(request, 'quiz_payments/create_product.html', context=context)

