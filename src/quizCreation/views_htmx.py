from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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

