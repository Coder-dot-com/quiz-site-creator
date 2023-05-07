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
    context['question_id'] = question_id

    if question.get_element_type()['type'] == 'Agree disagree table':

        context['mostly_agree_count'] = answers.filter(answer="Mostly agree").count()
        context['agree_count'] = answers.filter(answer="Agree").count()
        context['not_sure_count'] = answers.filter(answer="Not sure").count()
        context['disagree_count'] = answers.filter(answer="Disagree").count()
        context['mostly_disagree_count'] = answers.filter(answer="Mostly disagree").count()


        return render(request, 'quizData/answers/agree_disagree.html', context=context)
    


    elif question.get_element_type()['type'] == 'Satisfied unsatisfied table':

        context['mostly_satisfied_count'] = answers.filter(answer="Mostly satisfied").count()
        context['satisfied_count'] = answers.filter(answer="satisfied").count()
        context['not_sure_count'] = answers.filter(answer="Not sure").count()
        context['unsatisfied_count'] = answers.filter(answer="Unsatisfied").count()
        context['mostly_unsatisfied_count'] = answers.filter(answer="Mostly unsatisfied").count()


        return render(request, 'quizData/answers/satisfied_unsatisfied.html', context=context)


    elif question.get_element_type()['type'] == 'Multiple choice question':

        multiple_choice = question.get_element_type()['element']

        choices = multiple_choice.get_multiple_choice_choices()

        choices_count = []

        for choice in choices:
            choice_dict = {
                f'{choice.choice}': answers.filter(question_choice=choice.id).count()
            }

            choices_count.append(choice_dict)

        context['choices_count'] = choices_count
        return render(request, 'quizData/answers/multiple_choice.html', context=context)

    elif question.get_element_type()['type'] == 'Single choice question':

        single_choice = question.get_element_type()['element']

        choices = single_choice.get_single_choice_choices()

        choices_count = []

        for choice in choices:
            choice_dict = {
                f'{choice.choice}': answers.filter(single_question_choice=choice.id).count()
            }

            choices_count.append(choice_dict)

        context['choices_count'] = choices_count
        return render(request, 'quizData/answers/single_choice.html', context=context)


    else:
        return render(request, 'quizData/answers/all_other_questions.html', context=context)

