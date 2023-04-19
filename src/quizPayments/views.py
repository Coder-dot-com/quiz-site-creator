from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from django.shortcuts import render, redirect
from .forms import ProductCreateForm
from .models import Product
from django.contrib import messages

# Create your views here.
@login_required
def add_product_quiz(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)
    context = {
        'user_quiz': user_quiz,
    }
    product = None
    try:
        product = Product.objects.get(quiz=user_quiz)
        context['form'] = ProductCreateForm(instance=product),
        context['product'] = product       
    except Product.DoesNotExist:
        context['form'] = ProductCreateForm(),
        context['product']: False

    

    print(context)

    return render(request, 'quiz_payments/create_product_page.html', context=context)    



@login_required
def create_product(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    product = False

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



    messages.add_message(request, messages.SUCCESS, 'Product updated!')

    return redirect('add_product_quiz', quiz_id=quiz_id)

@login_required
def delete_product_quiz(request, quiz_id):
    user_quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    product = False

    try:
        product = Product.objects.get(quiz=user_quiz).delete()
    except Product.DoesNotExist:
        pass


    messages.add_message(request, messages.SUCCESS, 'Product deleted!')

    return redirect('add_product_quiz', quiz_id=quiz_id)