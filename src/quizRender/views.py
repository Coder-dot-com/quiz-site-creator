from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage

# Create your views here.
@login_required
def preview_quiz(request, quiz_id):

    quiz = UserQuiz.objects.filter(id=quiz_id, user=request.user)

    if quiz.exists():
        
        context = {}
        context['quiz_page'] = QuizPage.objects.get(number=1, quiz=quiz[0])
        return render(request, 'preview_quiz.html', context=context)
    
    else:
        return HttpResponse(500)