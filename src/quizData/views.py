from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from quizCreation.models import UserQuiz
from quizRender.models import Response
from itertools import chain


import csv
from io import StringIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.text import slugify
from django.views.generic import View
import math
# Create your views here.

@login_required
def view_quiz_results(request, quiz_id):

    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    responses = Response.objects.filter(quiz=quiz)
    response_count = responses.count()

    responses_completed = responses.filter(completed=True).count()

    percentage_completed = math.floor(responses_completed/response_count * 100)
    print(responses)
    context = {
        'responses': responses,
        'quiz': quiz,
        'response_count': response_count,
        'percentage_completed': percentage_completed,
    }
    return render(request, 'quizData/quiz_data.html', context=context)
                  

@login_required
def detailed_results(request, quiz_id, response_id):
    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    response = Response.objects.get(quiz=quiz, response_id=response_id)
    context = {
        'response': response,
        'quiz': quiz,

    }

    return render(request, 'quizData/response_details.html', context=context)

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

@login_required
def download_csv_of_responses(request, quiz_id):
    quiz = UserQuiz.objects.get(user=request.user, id=quiz_id)

    all_responses = Response.objects.filter(quiz=quiz).order_by('time_added')

    list_of_response_with_answers = []

    for r in all_responses:
        response_dict = { 'response_id': r.response_id,
                        'time_added': f"{r.time_added.time()} {r.time_added.date()} {r.time_added.tzinfo}",
                        'questions_and_answers': [],

        
        }
        answers = r.get_all_answers()

        for answers_query in answers:
            for a in answers_query:
                element = a.question.get_element_type()
                if not element['type'] == "Multiple choice question":
                    dict_to_append = {element['element'].title: a.answer}

                    response_dict['questions_and_answers'].append(dict_to_append)
                else:
                    answers_list = [x.choice for x in a.question_choice.all()]
                    dict_to_append = {element['element'].title: answers_list}
                    response_dict['questions_and_answers'].append(dict_to_append)

        list_of_response_with_answers.append(response_dict)

        keys  = list_of_response_with_answers[0].keys()
        
    with open('a.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_response_with_answers)

    with open('a.csv', 'r', newline='') as output_file:
                                 
        # response = StreamingHttpResponse(output_file,
        #                                 content_type="text/csv")
        # response['Content-Disposition'] = 'attachment; filename="{}"'.format('responses.csv')
        # return response

        response = HttpResponse(open("a.csv", 'rb').read())
        response['Content-Type'] = 'text/csv'
        response['Content-Disposition'] = 'attachment; filename=responses.csv'
        return response