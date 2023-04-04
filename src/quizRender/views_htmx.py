from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage
from uuid import uuid4


@login_required 
def next_page_preview(request, quiz_id, number, response_id=None):
    quiz = UserQuiz.objects.get(id=quiz_id)
    print(number)

    next_quiz_page = quiz.next_quiz_page(number=number)
    context = {}
    context['quiz_page']  = next_quiz_page
    context['first_page'] = False

    if request.user == quiz.user: #is preview
        
        return render(request, 'quiz_form.html', context=context)
    
    elif (response_id):
        return
    
    else:
        return HttpResponse(500)
    
@login_required 
def previous_page_preview(request, quiz_id, number, response_id=None):
    quiz = UserQuiz.objects.get(id=quiz_id)
    print(number)

    prev_quiz_page = quiz.previous_quiz_page(number=number)
    context = {}
    context['quiz_page']  = prev_quiz_page

    try:
        quiz.previous_quiz_page(number=prev_quiz_page.number)
        context['first_page'] = False
    except:
        print("first page is true")
        context['first_page'] = True

    if request.user == quiz.user: #is preview
        
        return render(request, 'quiz_form.html', context=context)
    
    elif (response_id):
        return
    
    else:
        return HttpResponse(500)