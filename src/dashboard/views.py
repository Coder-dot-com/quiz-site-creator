from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from dashboard.forms import AccountDetailsForm, ChangePasswordForm

from subscriptions.models import SubscriptionChoices, UserPaymentStatus, UserSubscriptions
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
import stripe
from quiz_site.settings import STRIPE_SECRET_KEY
from session_management.views import _session
from django.db.models import Q
from quizCreation.models import UserQuiz

stripe.api_key = STRIPE_SECRET_KEY



UserModel = get_user_model()

# Create your views here.

@login_required
def dashboard_home(request):
    context = {}
    
    quizes = UserQuiz.objects.filter(user=request.user)
    context['quizes'] = quizes

    return render(request, "dashboard2/index.html", context=context)


@login_required
def todays_overview(request):

    return render(request, 'dashboard2/pages/todays_overview.html')

@login_required
def subscription_page_dashboard(request):
    context = {}

    return render(request, 'dashboard2/subscription_page.html', context=context)


@login_required
def account_details_dashboard(request):
    user = request.user
    profile_obj = Profile.objects.get(user=user)

    if request.POST:
        form = AccountDetailsForm(request.POST)
    else:
        form = AccountDetailsForm(initial={'email': user.email})

    user = UserModel.objects.get(pk=request.user.id)

    if form.is_valid():
            email = form.cleaned_data.get('email')

            if email:
                user.email = email
                user.username = email
                user.save()
            
            messages.success(request, "Success, details updated!")
            profile_obj.save()

            return redirect('account_details_dashboard')

            
    
    context = {
        'form': form,
    }

    return render(request, 'dashboard2/account_details_dashboard.html', context=context)


@login_required
def change_password_dashboard(request):
    user = request.user

    form = ChangePasswordForm(request.POST or None)

    
    user = UserModel.objects.get(pk=request.user.id)

    if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
             
            if authenticate(request=None, username=user.username ,password=current_password):
                #change password to new password
                user.set_password(new_password)
                user.save()

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

                
                messages.success(request, "Success, password updated!")
            else:
                print("incorrct pass")
                messages.error(request, "Incorrect password")
     
    
    context = {
        'form': form,
    }

    return render(request, 'dashboard2/change_password_dashboard.html', context=context)


@login_required
def billing_history(request):
    user = request.user
    context = {}

    user_payment_status = UserPaymentStatus.objects.get(user=user)
    user_subscriptions =  UserSubscriptions.objects.filter(user_payment_status=user_payment_status).order_by('date_subscribed').reverse()

    invoices_data = []
    for subscription in user_subscriptions:
        subscription_id = subscription.subscription_id
        #Get all invoices associated with this and add to list
    
        subscription_invoices = stripe.Invoice.list(limit=100, subscription=subscription_id)
        print(subscription_invoices['data'][0]) #Last 0 is invoice number so check len if > 100
        #test this
        
        invoices = (subscription_invoices['data'])

        for invoice in invoices:
            unix_time = invoice['created']
            created = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
            if not invoice['amount_paid'] == 0:

                invoice_data = {

                    'amount_due': invoice['amount_paid']/100,
                    'currency': invoice['currency'],
                    'created': created,
                    'status': invoice['status'],
                    'link': invoice['hosted_invoice_url'],
                }
                invoices_data.append(invoice_data)


    context['invoices_data'] = invoices_data
        #if returned objects over limit then for loop with starting after to get others

    return render(request, 'dashboard2/billing_history.html', context=context)


