from datetime import datetime, timedelta, timezone

from django.urls import reverse
from emails.tasks import subscription_cancelled
from subscriptions.models import UserPaymentStatus, UserSubscriptions
from django.contrib import messages

def user_subscription_valid(request):
    expiry_date = None
    subscribe_url = None

    user = request.user
    subscribe_url = reverse('subscription_page_dashboard')

    try:
        user_payment_status = UserPaymentStatus.objects.get(user=user)
    except:
        return dict(checked_subscription=True)

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


 
        else:
            expiry_date = datetime.strftime(user_payment_status.subscription_expiry, '%Y-%m-%d')
  
    
        pass

 
    
    
    return dict(checked_subscription=True, user_payment_status=user_payment_status, subscribe_url=subscribe_url, expiry_date=expiry_date)


