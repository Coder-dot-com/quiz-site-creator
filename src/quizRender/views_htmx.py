from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz

@login_required
def preview_quiz_page(request, quiz_id):

    quiz = UserQuiz.objects.filter(id=quiz_id, user=request.user)

    if quiz.exists(): 
        context = {}
        return render(request, 'preview_quiz.html', context=context)
    
    else:
        return HttpResponse(500)