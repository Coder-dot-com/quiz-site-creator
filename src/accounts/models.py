from django.db import models

from django.contrib.auth import get_user_model
from datetime import timedelta, datetime, timezone

User = get_user_model()



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='profile')
    email_confirmed = models.BooleanField(default=False) 
    reset_password = models.BooleanField(default=False)

    def new_user(self):

        if datetime.now(timezone.utc) > self.user.date_joined + timedelta(days=1):
         return False
        else:
           return True


class UserPreferenceType(models.Model):
    preference_name = models.CharField(max_length=300, unique=True)
    def __str__(self):
        return self.preference_name




