from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from quizRender.models import Response
from itertools import chain
# Create your views here.

@login_required
def view_quiz_results(request, quiz_id):

    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    responses = Response.objects.filter(quiz=quiz)
    print(responses)
    context = {
        'responses': responses,
    }
    return render(request, 'quizData/quiz_data.html', context=context)
                  

@login_required
def detailed_results(request, quiz_id, response_id):
    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    response = Response.objects.get(quiz=quiz, response_id=response_id)
    context = {
        'response': response,
    }

    return render(request, 'quizData/response_details.html', context=context)