import datetime
from uuid import uuid4
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from session_management.models import  UserSession

import stripe
from emails.models import UserEmail
from quiz_site.settings import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY

from common.util.functions import event_id
from conversion_tracking.tasks import conversion_tracking
from django.contrib.auth import get_user_model, login
from django.contrib import messages

User = get_user_model()

stripe.api_key = STRIPE_SECRET_KEY
stripe_pub_key = STRIPE_PUBLIC_KEY


# Create your views here.


def _session(request):
    session_id = request.session.session_key
    if not session_id:

        request.session.save()
        session_id = request.session.session_key
    print("Session ID")
    print(session_id)
    
    if not session_id:
        session_id = uuid4()
    try:
        session = UserSession.objects.get(session_id=session_id)
    except UserSession.DoesNotExist:
        #Get refferer etc...

        session = UserSession.objects.create(session_id=session_id)
    except Exception as e:
        print("Error creating session")
        print(e)
    return session















