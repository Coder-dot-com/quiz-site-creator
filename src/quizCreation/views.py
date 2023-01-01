from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserQuiz
from django.shortcuts import redirect

# Create your views here.
@login_required
def create_quiz(request):
    return render(request, 'create_quiz.html')


@login_required
def quiz_edit(request, quiz_id):

    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)

    if user_quiz.exists():
        context = {
            'user_quiz': user_quiz,
        }
        return render(request, 'quiz_edit.html', context=context)

    redirect('dashboard_home')