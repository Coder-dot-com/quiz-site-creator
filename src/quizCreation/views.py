from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserQuiz, QuizPage
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
            'user_quiz': user_quiz[0], 
        }
        return render(request, 'quiz_edit.html', context=context)

    redirect('dashboard_home')

@login_required
def quiz_page_add(request, quiz_id):

    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    
    if user_quiz.exists():
        user_quiz = user_quiz[0]

        quiz_page_number = QuizPage.objects.filter(quiz=user_quiz).order_by('number')

        if quiz_page_number.exists():
            quiz_page_number = quiz_page_number[0].number
        else:
            quiz_page_number = 1
        quiz_page =  QuizPage.objects.create(quiz=user_quiz, number=(quiz_page_number+1))
        context = {
            'user_quiz': user_quiz,
            'quiz_page': quiz_page, 
        }
        return render(request, 'quiz_page_edit.html', context=context)

    return redirect('dashboard_home')


@login_required
def quiz_page_edit(request, quiz_id, page_id):

    user_quiz = UserQuiz.objects.filter(user=request.user, id=quiz_id)
    
    if user_quiz.exists():
        context = {
            'user_quiz': user_quiz[0],
            'page_id': page_id
        }
        return render(request, 'quiz_page_edit.html', context=context)

    redirect('dashboard_home')

