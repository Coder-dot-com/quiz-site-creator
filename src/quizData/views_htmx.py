from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from quizRender.models import Response

@login_required
def delete_response(request, quiz_id, response_id):

    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    try:
        Response.objects.get(quiz=quiz, response_id=response_id).delete()
    except Response.DoesNotExist:
        return HttpResponse(500)
    
    responses = Response.objects.filter(quiz=quiz)

    context = {
        'responses': responses,
        'deleted': True,
    }

    return render(request, 'quizData/response_table.html', context=context)