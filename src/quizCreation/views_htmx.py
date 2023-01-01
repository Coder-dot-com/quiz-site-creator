from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import UserQuiz

@login_required
def htmx_create_quiz(request):
    quiz_name = request.POST['quiz_name']
    user_quiz = UserQuiz.objects.create(name=quiz_name, user=request.user)

    context = {
        'user_quiz': user_quiz,
        'hx_url': f"/create_quiz/edit/{user_quiz.id}",
    }

    return render(request, 'questions_page.html', context=context)

@login_required
def quiz_page_element_add(request, quiz_id, page_id):

    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    
    if user_quiz.exists():
        #don't create the object yet just determine which element the user selected
        #  and pass the required form
        context = {
            'user_quiz': user_quiz[0], 
        }
        return render(request, 'quiz_page_edit.html', context=context)

    return HttpResponse("An error occured")