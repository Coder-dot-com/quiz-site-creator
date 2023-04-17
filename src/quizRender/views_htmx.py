from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage, QuizPageElement, MultipleChoiceChoice, SingleChoiceChoice, AgreeDisagreeRow
from uuid import uuid4
from .models import Response, Answer
from session_management.views import _session
from django.utils.datastructures import MultiValueDictKeyError



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

def take_next_page(request, quiz_id, number, response_id):
    quiz = UserQuiz.objects.get(id=quiz_id)
    current_quiz_page = QuizPage.objects.get(number=number, quiz=quiz)
    elements = current_quiz_page.get_quiz_page_elements()

    response_object = Response.objects.get_or_create(response_id=response_id, session=_session(request), quiz=quiz)[0]



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
        elif e.get_element_type()['type'] == "Agree disagree table":
            print("TEST")
            print(request.POST)
            questions = AgreeDisagreeRow.objects.filter(agree_disagree_element=e.get_element_type()['element'])
            for q in questions:
                answer_obj = Answer.objects.get_or_create(response=response_object, question_agree_disagree=q)[0]
                print(q.id)
                try:
                    answer = request.POST[str(q.id)]
                except MultiValueDictKeyError:
                    answer = ""  
                answer_obj.answer = answer
                answer_obj.save()       
        
        elif not e.get_element_type()['type'] == 'Text element':
            try:
                answer = request.POST[str(e.id)]
            except MultiValueDictKeyError:
                answer = ""            
            answer_obj.answer = answer
            answer_obj.save()
        
        
        elif e.get_element_type()['type'] == 'Text element':
            answer_obj.delete()    

        if e.get_element_type()['type'] == 'Email input element':
            email = request.POST[str(e.id)]
            session = _session(request)
            session.email = email
            session.save()
    
    response_object.steps_completed = number
    response_object.save()

    next_quiz_page = quiz.next_quiz_page(number=number)
    context = {}
    context['quiz_page']  = next_quiz_page
    context['first_page'] = False
    context['response_id'] = response_id
    

        
    return render(request, 'quiz_form.html', context=context)
    

    

    
def take_previous_page(request, quiz_id, number, response_id):
    quiz = UserQuiz.objects.get(id=quiz_id)

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
        

        
    return render(request, 'quiz_form.html', context=context)
    
    

def get_value_stored_in_db(request, quiz_id, element_id, response_id, question_id = None):
    context = {}
    element = QuizPageElement.objects.get(id=element_id)
    context['element']  = element
    context['response_id'] = response_id
    context['quiz_page'] = element.page
    context['checked_db'] = True

    response = Response.objects.get(session=_session(request), response_id=response_id)

    if not question_id:
        try:
            answer = Answer.objects.get(question=element, response=response)
        except Response.DoesNotExist:
            answer = False


    else:
        agree_disagree_question = AgreeDisagreeRow.objects.get(id=question_id)
        answer = Answer.objects.get(question_agree_disagree=agree_disagree_question, response=response)
        context['question'] = agree_disagree_question

    context['answer'] = answer

    if element.get_element_type()['type'] == "Char input element":
        return render(request, 'take_quiz_elements/char_input_element.html', context=context)
    elif element.get_element_type()['type'] == "Text input element":
        return render(request, 'take_quiz_elements/text_input_element.html', context=context)
    elif element.get_element_type()['type'] == "Number input element":
        return render(request, 'take_quiz_elements/number_input_element.html', context=context)
    elif element.get_element_type()['type'] == "Email input element":
        return render(request, 'take_quiz_elements/email_input_element.html', context=context)
    elif element.get_element_type()['type'] == "Multiple choice question":
        return render(request, 'take_quiz_elements/multiple_choice_input_element.html', context=context)
    elif element.get_element_type()['type'] == "Single choice question":
        return render(request, 'take_quiz_elements/single_choice_input_element.html', context=context)
    elif element.get_element_type()['type'] == "Agree disagree table":
        return render(request, 'take_quiz_elements/agree_disagree_row.html', context=context)
