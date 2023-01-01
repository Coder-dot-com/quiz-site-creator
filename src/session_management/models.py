from hashlib import blake2b
from uuid import uuid4
from django.db import models
from django.forms import CharField
from django.urls import reverse
from tinymce.models import HTMLField

from multicurrency.models import Currency
from django.contrib.auth import get_user_model

from accounts.models import UserPreferenceType
from emails.models import UserEmail

User = get_user_model()

# Create your models here.

class UserSession(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=250, blank=True, unique=True)
    time_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    email_obj = models.ForeignKey(UserEmail, blank=True, null=True, on_delete=models.SET_NULL)

    latest_fb_clid = models.CharField(max_length=500, blank=True, null=True)
    latest_fbp = models.CharField(max_length=500, blank=True, null=True)
    latest_t_clid = models.CharField(max_length=500, blank=True, null=True)
    ip = models.CharField(blank=True, max_length=2000, null=True)
    user_agent = models.CharField(blank=True, max_length=2000, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    country_code = models.CharField(max_length=250, blank=True, null=True)
    add_user_agent_to_exclusion_list = models.BooleanField(default=False)

    def convert_amount_to_session_currency(self, amount_in_usd):
        amount_in_usd = float(amount_in_usd)
        #Return the rounded amount same as on frontend
        return round(round(amount_in_usd * self.currency.one_usd_to_currency_rate), 2)


    def __str__(self) -> str:
        return self.session_id
    
    


class Referrer(models.Model):
    user_session = models.ForeignKey(UserSession, null=True, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=250, blank=True, null=True)
    audience = models.CharField(max_length=250, blank=True, null=True)
    ad = models.CharField(max_length=250, blank=True, null=True)


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    enable_pixels = models.BooleanField(default=True)
    analytics_base = models.TextField(max_length=5000, blank=True)
    analytics_content_view = models.TextField(max_length=5000, blank=True)
    analytics_lead = models.TextField(max_length=5000, blank=True)    
    # analytics_init_checkout = models.TextField(max_length=5000, blank=True)
    analytics_purchase = models.TextField(max_length=5000, blank=True)



    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.category_name


















