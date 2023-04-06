from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage
from uuid import uuid4
from session_management.views import _session
from .models import Response


# Create your views here.
@login_required
def preview_quiz(request, quiz_id):

    quiz = UserQuiz.objects.filter(id=quiz_id, user=request.user)

    if quiz.exists():
        
        context = {}
        context['quiz_page'] = quiz[0].first_quiz_page()
        context['first_page'] = True
        return render(request, 'preview_quiz.html', context=context)
    
    else:
        return HttpResponse(500)

def take_quiz(request, quiz_id):
    

    quiz = UserQuiz.objects.filter(id=quiz_id, user=request.user)

    if quiz.exists():
        
        context = {}
        context['quiz_page'] = quiz[0].first_quiz_page()
        context['first_page'] = True

        try:
            session = _session(request)
            response_id = Response.objects.filter(session=session, quiz__id=quiz_id, completed=False).latest('last_modified').response_id
        except Response.DoesNotExist:
            response_id = uuid4()

        context['response_id'] = response_id
        
        return render(request, 'take_quiz.html', context=context)
    
    else:
        return HttpResponse(500)
    
def complete_quiz(request, response_id):
    try:
        session = _session(request)
        response = Response.objects.filter(session=session, response_id=response_id).latest('last_modified')
    except Response.DoesNotExist:
        return HttpResponse(500)
    

    response.completed = True
    response.save()
    return render(request, 'quiz_completed.html')
                            

    
