from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from quizCreation.models import UserQuiz, QuizPage, MultipleChoiceChoice, SingleChoiceChoice
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
from common.util.functions import event_id
from quizConversionTracking.tasks import conversion_tracking_user_quiz

from quizPayments.models import Product

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
    except UserPaymentStatus.DoesNotExist:
        user_payment_status = None
        pass
    
    print(user_payment_status)

    print("Checking subscription")

        #The trigger for this function should be context_processors which checks for logged in,
        #user has an active User payment status and current time > subscription expiry,
        #been more than 10 minutes since last sync

    if user_payment_status and user_payment_status.status == "active" and datetime.now(timezone.utc) > (user_payment_status.subscription_expiry + timedelta(seconds=1)) and datetime.now(timezone.utc) > (user_payment_status.last_synced + timedelta(seconds=600)):
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
            
            pv_event_unique_id = event_id()
            vc_event_unique_id = event_id()

            context['pv_event_unique_id'] = pv_event_unique_id
            context['vc_event_unique_id'] = vc_event_unique_id


            event_source_url = request.META.get('HTTP_REFERER')

            session = _session(request)

            try:
                # Need to fix this to ensure different ids
                conversion_tracking_user_quiz.delay(event_name="PageView", event_id=pv_event_unique_id, event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)  
                conversion_tracking_user_quiz.delay(event_name="ViewContent", event_id=vc_event_unique_id, event_source_url=event_source_url,quiz_id=quiz_id, session_id=session.session_id)  

                print("tracking conversionuser quiz")
            except Exception as e:
                print("failed conv tracking")
                print(e)



            return render(request, 'take_quiz.html', context=context)
        else:
            return HttpResponse("The quiz owners subscription has expired. Quiz is currently unavailable")
    

    
    
def complete_quiz(request, quiz_id, number, response_id):

    quiz = UserQuiz.objects.get(id=quiz_id)
    current_quiz_page = QuizPage.objects.get(number=number, quiz=quiz)
    elements = current_quiz_page.get_quiz_page_elements()

    response_object = Response.objects.get_or_create(response_id=response_id, session=_session(request), quiz=quiz)[0]

    if not response_object.completed:
        for q in elements:
            answer_obj = Answer.objects.get_or_create(response=response_object, question=q)[0]

            if q.get_element_type()['type'] == 'Multiple choice question':
                answers_list = request.POST.getlist(str(q.id))
                answer = ", ".join(answers_list)
                answer_obj.answer = answer
                answer_obj.question_choice.clear()
                answer_obj.save()
                for i in answers_list:
                    element = q.get_element_type()['element']
                    question_choice = MultipleChoiceChoice.objects.get(
                            id=i)
                    answer_obj.question_choice.add(question_choice)
            
                answer_obj.save()

            elif q.get_element_type()['type'] == "Single choice question":
                print("SINGLE CHOICE")
                print(request.POST)
                try:
                    answer = request.POST[str(q.id)]
                    single_choice = SingleChoiceChoice.objects.get(id=answer)
                    answer = single_choice.choice
                    answer_obj.single_question_choice = single_choice
                except MultiValueDictKeyError:
                    answer = ""  
                answer_obj.answer = answer
                answer_obj.save()  

            elif not q.get_element_type()['type'] == 'Text':
                try:
                    answer = request.POST[str(q.id)]
                except MultiValueDictKeyError:
                    answer = ""
                answer_obj.answer = answer
                answer_obj.save()    
            
            
            elif q.get_element_type()['type'] == 'Text':
                answer_obj.delete()    

        
        response_object.steps_completed = number
        response_object.save()

    context = {}
    context['user_quiz'] = quiz
    context['response_id'] = response_id
    context['response'] = response_object
    try:
        product = Product.objects.get(quiz=quiz)
        context['product'] = product
    except Product.DoesNotExist:
        product = None


   
    response = response_object
    

    response.completed = True
    response.save()

    print("redirect")



    pv_event_unique_id = event_id()
    vc_event_unique_id = event_id()
    lead_event_unique_id = event_id()
    context['pv_event_unique_id'] = pv_event_unique_id
    context['vc_event_unique_id'] = vc_event_unique_id
    context['lead_event_unique_id'] = lead_event_unique_id
    event_source_url = request.META.get('HTTP_REFERER')
    session = _session(request)
    try:
        conversion_tracking_user_quiz.delay(event_name="PageView", event_id=pv_event_unique_id, event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)  
        conversion_tracking_user_quiz.delay(event_name="ViewContent", event_id=vc_event_unique_id, event_source_url=event_source_url,quiz_id=quiz_id, session_id=session.session_id)  
        conversion_tracking_user_quiz.delay(event_name="Lead", event_id=lead_event_unique_id, event_source_url=event_source_url,quiz_id=quiz_id, session_id=session.session_id)  
        print("tracking conversionuser quiz")
    except Exception as q:
        print("failed conv tracking")
        print(q)



    if quiz.redirect_url:
        return redirect(quiz.redirect_url)
    return render(request, 'quiz_completed.html', context=context)
                            

    
