from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage

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