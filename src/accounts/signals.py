from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from tiers.models import Tier

from subscriptions.models import UserPaymentStatus

from .models import Profile
from email_marketing.tasks import sync_email_with_sendinblue




@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        # profile.beta_tester = True
        profile.save()
        #Also create user payment status
        if not user.is_staff:
            tier = Tier.objects.get(type='professional')
            UserPaymentStatus.objects.create(user=user, status="free_trial", tier=tier)
        
        #Sync email with sib and also add to contacts list

        sync_email_with_sendinblue.delay(user.email)






    