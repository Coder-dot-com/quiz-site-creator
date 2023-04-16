from uuid import uuid4
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from emails.models import UserEmail

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import password_reset_token
from session_management.views import _session


from .forms import ChangePasswordForm, LoginForm, RegisterForm, ResetForm
from emails.tasks import password_reset_email
from common.util.functions import event_id

from conversion_tracking.tasks import conversion_tracking
from conversion_tracking.models import Category

# Create your views here.

UserModel = get_user_model()


def register_view(request):
    form =  RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('email')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        password2 = form.cleaned_data.get('password2')
        try:
            promo_consent = form.cleaned_data.get('promo_consent')
            promo_consent = True
        except:
            promo_consent = False


        try:
            user = UserModel.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            print("registration error")
            messages.error(request, "An error occured, please try again")
            print(e)
            user = None

        if user != None:
            old_session = _session(request)
            login(request, user)
            new_session = _session(request)

            #swap the session ids
            if not new_session.ip:
                new_id = new_session.session_id
                new_session.delete()
                old_session.session_id = new_id
            
            old_session.user = user
            old_session.save()

            # Create user emaillist object
            UserEmail.objects.create(user=user, email=email, promo_consent=promo_consent)
            
            messages.success(request, "Welcome, get started by using the menu")

            context = {}

            pv_event_unique_id = event_id()
            vc_event_unique_id = event_id()
            lead_event_unique_id = event_id()

            context['pv_event_unique_id'] = pv_event_unique_id
            context['vc_event_unique_id'] = vc_event_unique_id
            context['lead_event_unique_id'] = lead_event_unique_id


            event_source_url = request.META.get('HTTP_REFERER')

            session = _session(request)
            category = Category.objects.all()[0]

            try:
                # Need to fix this to ensure different ids
                conversion_tracking.delay(event_name="PageView", event_id=pv_event_unique_id, event_source_url=event_source_url, category_id=category.id, session_id=session.session_id)  
                conversion_tracking.delay(event_name="ViewContent", event_id=vc_event_unique_id, event_source_url=event_source_url, category_id=category.id, session_id=session.session_id)  
                conversion_tracking.delay(event_name="Lead", event_id=vc_event_unique_id, event_source_url=event_source_url, category_id=category.id, session_id=session.session_id)  

                print("tracking conversion")
            except Exception as e:
                print("failed conv tracking")
                print(e)

            #render dashboard home

            context['quizes'] = None

            return render(request, "dashboard2/index.html", context=context)

        else:
            request.session['register_error'] = 1
    return render(request, 'home_site2/register.html', {"form": form})



def login_view(request):
    form =  LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            old_session = _session(request)
            login(request, user)
            new_session = _session(request)

            #swap the session ids
            if not new_session.ip:
                new_id = new_session.session_id
                new_session.delete()
                old_session.session_id = new_id
            
            old_session.user = user
            old_session.save()

            return redirect('dashboard_home')
        else:
            messages.add_message(request, messages.WARNING, str("Incorrect login details, please try again"))
    return render(request, 'home_site2/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')

def reset_pass_request(request):
    form =  ResetForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')

        user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username))

       #Logic for token generation and email sending
    #    user.is_active = False  # User needs to be inactive for the reset password duration
        user = user[0]
        user.profile.reset_password = True
        user.save()

        reset_link = request.build_absolute_uri(reverse('reset_pass', kwargs={
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": password_reset_token.make_token(user)

        }))
        password_reset_email.delay(user, reset_link)

        messages.add_message(request, messages.SUCCESS, 'Request submitted, if this accounts exists, an email will be sent.')
    return render(request, 'home_site2/forgotten_pass.html', {"form": form})


def reset_pass(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str("An error occured"))
            print(e)
            user = None
        print('user', user)

        if user is not None and password_reset_token.check_token(user, token):
            form = ChangePasswordForm(data=request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data.get('password'))
                user.save()
                update_session_auth_hash(request, user)

                user.profile.reset_password = False
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return redirect('login_user')
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token
                }
                messages.add_message(request, messages.WARNING, 'Error password could not be reset.')
                return render(request, 'home_site2/change_pass.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
            messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print("User variable")
        print(UserModel)
        print(uid)
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str("An error occured"))
        print(e)
        user = None
    
    print(password_reset_token.check_token(user, token))
    if user is not None and password_reset_token.check_token(user, token):
        context = {
            'form': ChangePasswordForm(),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'home_site2/change_pass.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
        messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

    return redirect('reset_pass_request')
