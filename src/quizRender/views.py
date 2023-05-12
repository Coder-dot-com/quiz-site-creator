from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from quizCreation.models import UserQuiz, QuizPage, MultipleChoiceChoice, SingleChoiceChoice, AgreeDisagreeRow, SatisfiedUnsatisfiedRow, DropdownChoice
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

from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt
def take_quiz(request, quiz_id):

    quiz = UserQuiz.objects.filter(id=quiz_id)

    user = quiz[0].user
    # check user payment status is

    try:
        user_payment_status = UserPaymentStatus.objects.get(user=user)
    except UserPaymentStatus.DoesNotExist:
        user_payment_status = None
        pass

    print(user_payment_status)

    print("Checking subscription")

    # The trigger for this function should be context_processors which checks for logged in,
    # user has an active User payment status and current time > subscription expiry,
    # been more than 10 minutes since last sync

    if user_payment_status and user_payment_status.status == "active" and datetime.now(timezone.utc) > (user_payment_status.subscription_expiry + timedelta(seconds=1)) and datetime.now(timezone.utc) > (user_payment_status.last_synced + timedelta(seconds=600)):
        response = user_payment_status.sync_subscription_expiry()
        if response == "Canceled":
            try:
                user_subscription = UserSubscriptions.objects.filter(
                    user_payment_status=user_payment_status,
                ).latest('created_at')
                subscription_cancelled.delay(
                    user_subscription.subscription_id, failed_payment=True)
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
        if user_payment_status.status == "free_trial" or user_payment_status.status == "active":

            context = {}
            context['quiz'] = quiz[0]
            context['quiz_page'] = quiz[0].first_quiz_page()
            context['first_page'] = True

            try:
                session = _session(request)
                response_id = Response.objects.filter(
                    session=session, quiz__id=quiz_id, completed=False).latest('last_modified').response_id
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
                conversion_tracking_user_quiz.delay(event_name="PageView", event_id=pv_event_unique_id,
                                                    event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)
                conversion_tracking_user_quiz.delay(event_name="ViewContent", event_id=vc_event_unique_id,
                                                    event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)

                print("tracking conversionuser quiz")
            except Exception as e:
                print("failed conv tracking")
                print(e)

            return render(request, 'take_quiz.html', context=context)
        else:
            return HttpResponse("The quiz owners subscription has expired. Quiz is currently unavailable")

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@xframe_options_exempt
def complete_quiz(request, quiz_id, number, response_id):
    context = {}

    quiz = UserQuiz.objects.get(id=quiz_id)
    current_quiz_page = QuizPage.objects.get(number=number, quiz=quiz)
    elements = current_quiz_page.get_quiz_page_elements()

    response_object = Response.objects.filter(
        response_id=response_id, quiz=quiz)
    
    print(response_object)

    if response_object.exists() and request.POST:
        if response_object[0].completed:
            print("redirect")
            return redirect('take_quiz', quiz_id=quiz_id)

    if not response_object.exists() and QuizPage.objects.filter(quiz=quiz).count() == 1 and request.POST:
        Response.objects.create(response_id=response_id,
                                session=_session(request), quiz=quiz)
        response_object = Response.objects.filter(
            response_id=response_id, session=_session(request), quiz=quiz)

    print('response_object', response_object)

    if response_object.exists() and request.method == 'POST':
        response_object = response_object[0]

        for e in elements:

            if e.get_element_type()['type'] == 'Multiple choice question':
                answer_obj = Answer.objects.get_or_create(response=response_object, question=e)[0]
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
            elif e.get_element_type()['type'] == "Single choice question":
                answer_obj = Answer.objects.get_or_create(response=response_object, question=e)[0]
                try:
                    answer = request.POST[str(e.id)]
                    single_choice = SingleChoiceChoice.objects.get(id=answer)
                    answer = single_choice.choice
                    answer_obj.single_question_choice = single_choice
                except MultiValueDictKeyError:
                    answer = ""  
                answer_obj.answer = answer
                answer_obj.save()  
            
            elif e.get_element_type()['type'] == "Dropdown":
                answer_obj = Answer.objects.get_or_create(response=response_object, question=e)[0]
                try:
                    answer = request.POST[str(e.id)]
                    dropdown_choice = DropdownChoice.objects.get(id=answer)
                    answer = dropdown_choice.choice
                    answer_obj.dropdown_choice = dropdown_choice
                except MultiValueDictKeyError:
                    answer = ""  
                answer_obj.answer = answer
                answer_obj.save()   
            elif e.get_element_type()['type'] == "Agree disagree table":
                questions = AgreeDisagreeRow.objects.filter(agree_disagree_element=e.get_element_type()['element'])
                for q in questions:
                    answer_obj = Answer.objects.get_or_create(response=response_object, question_agree_disagree=q, question=e)[0]
                    print(q.id)
                    try:
                        answer = request.POST[str(q.id)]
                        answer_obj.answer = answer
                        answer_obj.save()
                    except MultiValueDictKeyError:
                        answer_obj.delete()

            elif e.get_element_type()['type'] == "Satisfied unsatisfied table":
                questions = SatisfiedUnsatisfiedRow.objects.filter(satisfied_unsatisfied_element=e.get_element_type()['element'])
                for q in questions:

                    answer_obj = Answer.objects.get_or_create(response=response_object, question_satisfied_unsatisfied=q, question=e)[0]
                    print(q.id)
                    try:
                        answer = request.POST[str(q.id)]
                        answer_obj.answer = answer
                        answer_obj.save()
                    except MultiValueDictKeyError:
                        answer_obj.delete()             
            
            elif not e.get_element_type()['type'] == 'Text':
                answer_obj = Answer.objects.get_or_create(response=response_object, question=e)[0]
                try:
                    answer = request.POST[str(e.id)]
                except MultiValueDictKeyError:
                    answer = ""            
                answer_obj.answer = answer
                answer_obj.save()
            

            if e.get_element_type()['type'] == 'Email input':
                email = request.POST[str(e.id)]
                session = _session(request)
                session.email = email
                session.save()
    

        response_object.steps_completed = number
        response_object.completed = True
        response_object.save()

        pv_event_unique_id = event_id()
        vc_event_unique_id = event_id()
        lead_event_unique_id = event_id()
        context['pv_event_unique_id'] = pv_event_unique_id
        context['vc_event_unique_id'] = vc_event_unique_id
        context['lead_event_unique_id'] = lead_event_unique_id
        event_source_url = request.META.get('HTTP_REFERER')
        session = _session(request)
        try:
            conversion_tracking_user_quiz.delay(event_name="PageView", event_id=pv_event_unique_id,
                                                event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)
            conversion_tracking_user_quiz.delay(event_name="ViewContent", event_id=vc_event_unique_id,
                                                event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)
            conversion_tracking_user_quiz.delay(event_name="Lead", event_id=lead_event_unique_id,
                                                event_source_url=event_source_url, quiz_id=quiz_id, session_id=session.session_id)
            print("tracking conversionuser quiz")
        except Exception as q:
            print("failed conv tracking")
            print(q)


    
    context['user_quiz'] = quiz
    context['response_id'] = response_id

    
    try:
        product = Product.objects.get(quiz=quiz)
        context['product'] = product
    except Product.DoesNotExist:
        product = None


    if quiz.redirect_url:
        return redirect(quiz.redirect_url)
    return render(request, 'quiz_completed.html', context=context)
