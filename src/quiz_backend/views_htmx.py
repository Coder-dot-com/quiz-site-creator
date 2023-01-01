import datetime
from uuid import uuid4
from django.shortcuts import render, HttpResponse
from django.urls import reverse

from multicurrency.models import Currency
from session_management.models import Category

from .models import Answer, Question, QuestionChoice, Quiz, QuizOrder, Response, UserImageUpload
from session_management.views import _session
import os

from conversion_tracking.tasks import conversion_tracking
from emails.models import UserEmail
import stripe
from quiz_site.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY
from common.util.functions import event_id

stripe.api_key = STRIPE_SECRET_KEY
stripe_pub_key = STRIPE_PUBLIC_KEY


def quiz_without_question_num(request, unique_id):
    context = {}

    context['question'] = Question.objects.get(
        quiz__unique_id=unique_id,  number=1)
    response_id = uuid4()
    context['response_id'] = response_id
    return render(request, 'quiz_backend/question.html', context=context)


def go_back_question(request, unique_id, question_id, response):
    question = Question.objects.get(quiz__unique_id=unique_id, id=question_id)
    previous_question = Question.objects.get(
        quiz__unique_id=unique_id, number=question.number - 1)

    context = {}
    context['question'] = previous_question
    context['response_id'] = response
    previous_answer = None

    try:
        previous_answer = Answer.objects.get(
            response__response_id=response, question=previous_question)
        context['previous_answer'] = previous_answer
    except:
        pass
    if previous_answer:
        if previous_answer.get_user_images():
            previous_images = previous_answer.get_user_images()
            context['user_image_count'] = previous_images.count()
            context['user_images'] = previous_images

    return render(request, 'quiz_backend/question.html', context=context)


def go_back_quiz_end(request, unique_id, response):

    previous_question = Question.objects.filter(
        quiz__unique_id=unique_id).order_by('-number').first()

    context = {}
    context['question'] = previous_question
    context['response_id'] = response
    previous_answer = None

    try:
        previous_answer = Answer.objects.get(
            response__response_id=response, question=previous_question)
        context['previous_answer'] = previous_answer
    except:
        pass
    if previous_answer:
        if previous_answer.get_user_images():
            previous_images = previous_answer.get_user_images()
            context['user_image_count'] = previous_images.count()
            context['user_images'] = previous_images

    return render(request, 'quiz_backend/question.html', context=context)

def go_back_purchase(request, response_id):
    context = {}
    response = Response.objects.get(response_id=response_id)
    context['quiz'] = response.quiz
    context['response_id'] = response.response_id

    session = _session(request)
    price_usd = response.quiz.product.price
    price_without_discount_usd = response.quiz.product.price_without_discount
    if price_usd:
        price = session.convert_amount_to_session_currency(
            price_usd)
        price_without_discount_converted = None
        if price_without_discount_usd:
            price_without_discount_converted = session.convert_amount_to_session_currency(
                price_without_discount_usd)

        context['price'] =  f'{price: .2f}'
        context['price_without_discount_converted'] =  f'{price_without_discount_converted: .2f}'
        
    return render(request, 'quiz_backend/quiz_end.html', context=context)


def submit_question(request, unique_id, question_id):

    question = Question.objects.get(quiz__unique_id=unique_id, id=question_id)

    # Create the response object and answer

    session = _session(request)
    if request.POST:
        response_id = request.POST['response']
    else:
        response_id = request.GET['response']

    response, created = Response.objects.get_or_create(
        quiz=question.quiz, response_id=response_id, session=session)
    if request.POST:
        # Will need to pass through the response id

        # Lopgic will vary depending on question type
        answer_obj, created = Answer.objects.get_or_create(
            response=response, question=question)
        print(request.POST)

        if question.type == "Multiple Choice":
            answers_list = request.POST.getlist(question_id)
            answer = ", ".join(answers_list)
            answer_obj.answer = answer
            answer_obj.question_choice.clear()
            answer_obj.save()
            for i in answers_list:
                try:
                    question_choice = QuestionChoice.objects.get(
                        question=question, option=i)
                    answer_obj.question_choice.add(question_choice)
                except Exception as e:
                    print(e)
                    pass
            answer_obj.save()

        elif question.type == 'Email Input':
            answer = request.POST[question_id]
            answer_obj.answer = answer
            answer_obj.save()
            # Also add a consent checkbox
            try:
                email_consent = bool(request.POST['email_consent'])
            except:
                email_consent = False
            try:
                email_obj = UserEmail.objects.get(email=answer)
                email_obj.promo_consent = email_consent
                email_obj.save()
            except UserEmail.DoesNotExist:
                email_obj = UserEmail.objects.create(
                    email=answer, promo_consent=email_consent)
            session.email_obj = email_obj
            session.email = answer
            session.save()
        elif  question.type == 'Sales Page':
            pass
        else:
            answer = request.POST[question_id]
            answer_obj.answer = answer
            answer_obj.save()
            try:
                question_choice = QuestionChoice.objects.get(
                    question=question, option=answer)
                answer_obj.question_choice.add(question_choice)
            except Exception as e:
                print(e)
                pass

    # Then render the next question
    context = {}

    # I.e. image input question
    if request.GET:
        # Check if required image has been added
        if not question.skippable:
            try:
                answer = Answer.objects.get(
                    response=response, question=question)
                user_images = UserImageUpload.objects.filter(
                    answer=answer).count()
                if user_images == 0:
                    raise ValueError  # raise error if no images uploaded
            except:
                context['question'] = question
                # Means it's image
                context['response_id'] = response_id
                context['error'] = True
                return render(request, 'quiz_backend/question.html', context=context)

    try:
        next_question = Question.objects.get(
            quiz__unique_id=unique_id, number=question.number + 1)
        context['question'] = next_question
        # Means it's image

        # Check if last question
        try:
            next_next_question = Question.objects.get(
                quiz__unique_id=unique_id, number=next_question.number + 1)
        except Question.DoesNotExist:
            context['last_question'] = True
        context['response_id'] = response_id
        # Check for existing answers
        try:
            next_answer = Answer.objects.get(
                response=response, question=next_question)
            context['previous_answer'] = next_answer
        except:
            next_answer = None
        if next_answer:
            if next_answer.get_user_images():
                next_images = next_answer.get_user_images()
                context['user_image_count'] = next_images.count()
                context['user_images'] = next_images


        return render(request, 'quiz_backend/question.html', context=context)

    except Question.DoesNotExist:
        # Means is last question so render quiz success
        context['quiz'] = question.quiz
        context['response_id'] = response_id
        session = _session(request)

        if response.quiz.product and not response.quiz.product.type == 'user_chosen':
            price_usd = response.quiz.product.price
            price_without_discount_usd = response.quiz.product.price_without_discount

            price = session.convert_amount_to_session_currency(
                price_usd)
            price_without_discount_converted = None
            if price_without_discount_usd:
                price_without_discount_converted = session.convert_amount_to_session_currency(
                    price_without_discount_usd)

            context['price'] =  f'{price: .2f}'
            context['price_without_discount_converted'] =  f'{price_without_discount_converted: .2f}'
        response.completed = True
        response.save()
            
        event_source_url = request.META.get('HTTP_REFERER')


        lead_event_id = event_id()
        context['lead_event_id'] = lead_event_id
        print("lead")
        category = Category.objects.all()[0]
        context['category'] = category
        conversion_tracking.delay(event_name="Lead", event_id=lead_event_id, event_source_url=event_source_url, category_id=category.id, session_id=session.session_id)  


        return render(request, 'quiz_backend/quiz_end.html', context=context)


def chosen_currency_quiz_end(request, currency_code, response_id):
    context = {}
    session = _session(request)
    session = _session(request)
    try: 
        currency_code = Currency.objects.get(currency_code=currency_code)
    except Exception as e:
        print("error when setting currency", e)
        return HttpResponse(500)
        
    try: 
        session.currency = currency_code
        session.save()     
    except Exception as e:
        print("error when setting currency", e)
        return HttpResponse(500)

    response, created = Response.objects.get_or_create(
         response_id=response_id, session=session)
    context['quiz'] = response.quiz
    context['response_id'] = response_id
    session = _session(request)
    price_usd = response.quiz.product.price
    price_without_discount_usd = response.quiz.product.price_without_discount
    
    if price_usd:
        price = session.convert_amount_to_session_currency(
            price_usd)
        price_without_discount_converted = None
        if price_without_discount_usd:
            price_without_discount_converted = session.convert_amount_to_session_currency(
                price_without_discount_usd)

        context['price'] =  f'{price: .2f}'
        context['price_without_discount_converted'] =  f'{price_without_discount_converted: .2f}'

    return render(request, 'quiz_backend/quiz_end.html', context=context)

def image_upload(request, unique_id, question_id, response_id):
    print("Image upload")

    quiz = Quiz.objects.get(unique_id=unique_id)

    # Get the response or create
    session = _session(request)

    try:
        response = Response.objects.get(
            quiz=quiz, response_id=response_id, session=session)
    except:
        response = Response.objects.create(
            quiz=quiz, response_id=response_id, session=session)

    # Get the answer for the question if not then create
    too_many_images = False

    for question_id in request.FILES:
        if question_id.startswith('image_'):
            question_db_id = question_id.split('_')[-1]
            question = Question.objects.get(id=question_db_id)
            try:
                answer_obj = Answer.objects.get(
                    response=response, question=question)
            except:
                answer_obj = Answer()
                answer_obj.question = question
                answer_obj.response = response
                answer_obj.save()

            images = request.FILES.getlist(question_id)

            for image in images:
                if image.size < 20000000 and image.size > 100:
                    file_name = image.name
                    file_ext = os.path.splitext(file_name)[1]
                    if file_ext == '.jpeg':
                        file_ext = '.jpg'

                    image.name = f"{uuid4()}{file_ext}"
                    if UserImageUpload.objects.filter(answer=answer_obj).count() < question.image_upload_number:
                        UserImageUpload.objects.create(
                            image=image, answer=answer_obj)
                    else:
                        too_many_images = True

    user_images = UserImageUpload.objects.filter(answer=answer_obj)
    user_image_count = user_images.count()
    context = {
        'quiz': quiz,
        'question': question,
        'response_id': response_id,
        'user_images': user_images,
        'user_image_count': user_image_count,
        'too_many_images': too_many_images,


    }
    return render(request, 'quiz_backend/htmx_image.html', context=context)


def delete_image(request, unique_id, response_id, user_image_id):
    session = _session(request)
    quiz = Quiz.objects.get(unique_id=unique_id)

    try:
        response = Response.objects.get(
            quiz=quiz, response_id=response_id, session=session)
    except:
        return HttpResponse(500)

    user_image = UserImageUpload.objects.get(
        answer__response=response, id=user_image_id)
    user_image.delete()
    question = user_image.answer.question

    user_images = UserImageUpload.objects.filter(answer=user_image.answer)
    user_image_count = user_images.count()

    context = {
        'quiz': quiz,
        'question': question,
        'response_id': response_id,
        'user_images': user_images,
        'user_image_count': user_image_count,
    }
    return render(request, 'quiz_backend/htmx_image.html', context=context)


def checkout(request, unique_id, response_id):
    quiz = Quiz.objects.get(unique_id=unique_id)
    session = _session(request)
    payment_intent_id = None
    try:
        response = Response.objects.get(
            response_id=response_id, session=session)
    except Exception as e:
        print(e)
        return HttpResponse('An error occured: quiz response not found, please refresh and retake the quiz to try again')

    price_without_discount_converted = None
    price_without_discount_usd = None
    if response.quiz.product.type == 'user_chosen':
        user_selected_price = float(request.POST['user_selected_price'])
        interval = float(request.POST['interval'])
        price = user_selected_price * interval
        price_usd =  price/session.currency.one_usd_to_currency_rate
        print(price)

    else:
        price_usd = quiz.product.price

        price_without_discount_usd = quiz.product.price_without_discount

        price = session.convert_amount_to_session_currency(
            price_usd)
        if price_without_discount_usd:
            price_without_discount_converted = session.convert_amount_to_session_currency(
                price_without_discount_usd)


    currency = session.currency

    # Create stripe customer if product subscription
    if quiz.product.type == "subscription":
        price_id = quiz.product.stripe_price_id
        customer = stripe.Customer.create(
            email=response.session.email_obj.email,
        )
        print('customer', customer)
        customer_id = customer.id
        print(customer_id)
        try:
            # Create the subscription. Note we're expanding the Subscription's
            # latest invoice and that invoice's payment_intent
            # so we can pass it to the front end to confirm the payment
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{
                    'price': price_id,
                }],
                trial_period_days=quiz.product.days_free_trial,
                # trial_end=1652631902,
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )
            payment_intent_id = subscription.id

            if quiz.product.days_free_trial:
                setup_intent = stripe.SetupIntent.create(
                    customer=customer_id,
                    payment_method_types=["card"],
                    usage='off_session'
                )
                client_secret = setup_intent.client_secret
            else:
                client_secret = subscription.latest_invoice.payment_intent.client_secret
        except Exception as e:
            print(e)

        # Create payment intent
    else:

        intent = stripe.PaymentIntent.create(
            amount=int(price*100),
            currency=currency,
            payment_method_types=[
                "card",
            ],
            metadata={
            'email': session.email_obj.email,
        },
        )

        client_secret = intent.client_secret
        payment_intent_id = intent.id

    # Create the order object here and order num
    yr = int(datetime.date.today().strftime('%Y'))
    dt = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d = datetime.date(yr, mt, dt)
    current_date = d.strftime("%Y%m%d")

    order = QuizOrder()

    order.product = quiz.product
    order.response = response
    order.email = response.session.email_obj
    order.order_total = price
    order.currency = currency
    order.total_usd = price_usd
    if response.quiz.product.type == 'user_chosen':
        order.user_chosen_price_per_month = float(request.POST['user_selected_price'])
        order.user_chosen_interval_months = int(request.POST['interval'])
    if payment_intent_id:
        order.payment_intent_id = payment_intent_id

    order.save()
    order.order_number = current_date + str(order.id)
    order.save()
    order.session = session
    order.save()

    # Create new url and view, template for success from quiz purchase

    return_url = request.build_absolute_uri(reverse('quiz_payment_success'))

    # Conv tracking

    event_source_url = request.META.get('HTTP_REFERER')
    print("Source URL for product view")
    print(event_source_url)

    event_unique_id = event_id()
    session = _session(request)

    try:
        conversion_tracking.delay(event_name="InitiateCheckout", event_id=event_unique_id,
                                  event_source_url=event_source_url, category_id=quiz.category.id, session_id=session.session_id)
        print("tracking conversion")

    except Exception as e:
        print("failed conv tracking")
        print(e)

    context = {
        'quiz': quiz,
        'response': response,
        'client_secret': client_secret,
        'stripe_pub_key': stripe_pub_key,
        'return_url': return_url,
        'event_id': event_unique_id,
        'order': order,

    }

    price_without_discount_converted = None
    if price_without_discount_usd:
        price_without_discount_converted = session.convert_amount_to_session_currency(
            price_without_discount_usd)

    context['final_price_converted'] = price

    if price_without_discount_converted:
        context['price_without_discount_converted'] = price_without_discount_converted

    context['response_id'] = response.response_id

    return render(request, 'quiz_backend/purchase.html', context=context)




