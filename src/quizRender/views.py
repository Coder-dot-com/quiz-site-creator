from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from quizCreation.models import UserQuiz, QuizPage, MultipleChoiceChoice
from subscriptions.models import UserPaymentStatus
from datetime import datetime
from uuid import uuid4
from session_management.views import _session
from .models import Response, Answer
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, timedelta, timezone

from django.urls import reverse
from emails.tasks import subscription_cancelled
from subscriptions.models import UserPaymentStatus, UserSubscriptions
# Create your views here.
@login_required
def preview_quiz(request, quiz_id):

    quiz = UserQuiz.objects.filter(id=quiz_id, user=request.user)

    if quiz.exists():
        
        context = {}
        context['quiz_page'] = quiz[0].first_quiz_page()
        context['first_page'] = True
        return render(request, 'preview_quiz.html', context=context)


def take_quiz(request, quiz_id):
    

    quiz = UserQuiz.objects.filter(id=quiz_id)

    user = quiz[0].user
    #check user payment status is 
    
    try:
        user_payment_status = UserPaymentStatus.objects.get(user=user)
    except:
        return dict(checked_subscription=True)
    
    print(user_payment_status)

    print("Checking subscription")

        #The trigger for this function should be context_processors which checks for logged in,
        #user has an active User payment status and current time > subscription expiry,
        #been more than 10 minutes since last sync

    if user_payment_status.status == "active" and datetime.now(timezone.utc) > (user_payment_status.subscription_expiry + timedelta(seconds=1)) and datetime.now(timezone.utc) > (user_payment_status.last_synced + timedelta(seconds=600)):
        response = user_payment_status.sync_subscription_expiry()
        if response == "Canceled":
            try:
                user_subscription = UserSubscriptions.objects.filter(
                user_payment_status=user_payment_status,
                ).latest('created_at')
                subscription_cancelled.delay(user_subscription.subscription_id, failed_payment=True)
            except Exception as b:
                print(b)
 
    elif user_payment_status.status == "free":
        response = user_payment_status.sync_subscription_expiry()

 
    elif user_payment_status.status == "free_trial":
        subscribe_url = reverse('subscription_page_dashboard')
        if user_payment_status.subscription_expiry.replace(tzinfo=None) < datetime.utcnow().replace(tzinfo=None):
            user_payment_status.status = "free"
            user_payment_status.save()
            print(user_payment_status.status)
            print("TEST1231")




    if quiz.exists():
        if user_payment_status.status == "free_trial" or  user_payment_status.status == "active":

        
            context = {}
            context['quiz_page'] = quiz[0].first_quiz_page()
            context['first_page'] = True

            try:
                session = _session(request)
                response_id = Response.objects.filter(session=session, quiz__id=quiz_id, completed=False).latest('last_modified').response_id
            except Response.DoesNotExist:
                response_id = uuid4()

            context['response_id'] = response_id
            
            print("TAKE UQUIZ")
            
            return render(request, 'take_quiz.html', context=context)
        else:
            return HttpResponse("The quiz owners subscription has expired. Quiz is currently unavailable")
    

    
    
def complete_quiz(request, quiz_id, number, response_id):

    quiz = UserQuiz.objects.get(id=quiz_id)
    current_quiz_page = QuizPage.objects.get(number=number, quiz=quiz)
    elements = current_quiz_page.get_quiz_page_elements()

    response_object = Response.objects.get_or_create(response_id=response_id, session=_session(request), quiz=quiz)[0]

    print(request.POST)

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
            try:
                answer = request.POST[str(e.id)]
            except MultiValueDictKeyError:
                answer = ""
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
   
    response = response_object
    

    response.completed = True
    response.save()
    return render(request, 'quiz_completed.html')
                            

    
