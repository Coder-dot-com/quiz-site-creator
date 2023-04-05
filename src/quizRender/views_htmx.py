from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage, MultipleChoiceChoice
from uuid import uuid4
from .models import Response, Answer


@login_required 
def next_page_preview(request, quiz_id, number):
    quiz = UserQuiz.objects.get(id=quiz_id)
    print(number)

    next_quiz_page = quiz.next_quiz_page(number=number)
    context = {}
    context['quiz_page']  = next_quiz_page
    context['first_page'] = False

    if request.user == quiz.user: #is preview
        
        return render(request, 'quiz_form.html', context=context)
    

    
    else:
        return HttpResponse(500)
    
@login_required 
def previous_page_preview(request, quiz_id, number):
    quiz = UserQuiz.objects.get(id=quiz_id)
    print(number)

    prev_quiz_page = quiz.previous_quiz_page(number=number)
    context = {}
    context['quiz_page']  = prev_quiz_page

    try:
        quiz.previous_quiz_page(number=prev_quiz_page.number)
        context['first_page'] = False
    except:
        print("first page is true")
        context['first_page'] = True

    if request.user == quiz.user: #is preview
        
        return render(request, 'quiz_form.html', context=context)
    
    else:
        return HttpResponse(500)
    

@login_required 
def take_next_page(request, quiz_id, number, response_id):
    quiz = UserQuiz.objects.get(id=quiz_id)
    print(request.POST)
    print('take_next_page')
    current_quiz_page = QuizPage.objects.get(number=number, quiz=quiz)
    elements = current_quiz_page.get_quiz_page_elements()

    response_object = Response.objects.get_or_create(response_id=response_id)[0]



    for e in elements:
        answer_obj = Answer.objects.get_or_create(response=response_object, question=e)[0]

        if e.get_element_type()['type'] == 'Multiple choice question':
            answers_list = request.POST.getlist(str(e.id))
            answer = ", ".join(answers_list)
            answer_obj.answer = answer
            answer_obj.question_choice.clear()
            answer_obj.save()
            for i in answers_list:
                element = e.get_element_type()['element']
                question_choice = MultipleChoiceChoice.objects.get(
                        id=i)
                answer_obj.question_choice.add(question_choice)
           
            answer_obj.save()
        elif not e.get_element_type()['type'] == 'Text element':
            answer = request.POST[str(e.id)]
            answer_obj.answer = answer
            answer_obj.save()    
        
        
        elif e.get_element_type()['type'] == 'Text element':
            answer_obj.delete()    

    
    response_object.steps_completed = number
    response_object.save()

    next_quiz_page = quiz.next_quiz_page(number=number)
    context = {}
    context['quiz_page']  = next_quiz_page
    context['first_page'] = False
    context['response_id'] = response_id

    if request.user == quiz.user: #is preview
        
        return render(request, 'quiz_form.html', context=context)
    

    
    else:
        return HttpResponse(500)
    
@login_required 
def take_previous_page(request, quiz_id, number, response_id):
    quiz = UserQuiz.objects.get(id=quiz_id)
    print(number)

    prev_quiz_page = quiz.previous_quiz_page(number=number)
    context = {}
    context['quiz_page']  = prev_quiz_page
    context['response_id'] = response_id

    try:
        quiz.previous_quiz_page(number=prev_quiz_page.number)
        context['first_page'] = False
    except:
        print("first page is true")
        context['first_page'] = True

    if request.user == quiz.user: #is preview
        
        return render(request, 'quiz_form.html', context=context)
    
    else:
        return HttpResponse(500)
    