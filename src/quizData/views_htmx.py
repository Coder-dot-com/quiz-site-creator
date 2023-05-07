from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz, QuizPageElement
from quizRender.models import Response, Answer

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
        'quiz': quiz,
    }

    return render(request, 'quizData/response_table.html', context=context)

@login_required
def get_question_answers(request, quiz_id, question_id):

    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)
    question =  QuizPageElement.objects.get(page__quiz=quiz, id=question_id)
    
    answers = Answer.objects.filter(question=question)
    context = {}
    context['answers']  = answers

    if question.get_element_type()['type'] == 'Char input':
        return render(request, 'quizData/answers/char_input.html', context=context)
    elif question.get_element_type()['type'] == 'Agree disagree table':

        context['mostly_agree_count'] = answers.filter(answer="Mostly agree").count()
        context['agree_count'] = answers.filter(answer="Agree").count()
        context['not_sure_count'] = answers.filter(answer="Not sure").count()
        context['disagree_count'] = answers.filter(answer="Disagree").count()
        context['mostly_disagree_count'] = answers.filter(answer="Mostly disagree").count()


        return render(request, 'quizData/answers/agree_disagree.html', context=context)


    return HttpResponse(f"TEST {question_id}")
