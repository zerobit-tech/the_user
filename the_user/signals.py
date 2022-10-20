from django.contrib.auth.models import User
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in, password_changed, password_reset, email_confirmed, \
    email_confirmation_sent, email_changed
from .models import BooleanSettings, Profile
from django.dispatch import receiver
import logging
logger = logging.getLogger('ilogger')

def create_profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile =Profile.objects.create(user=user)
    
    return profile


@receiver(post_save, sender=User)
def on_save_user_profile(sender, instance,created, **kwargs):
    # create user profile
    user = instance
 
    create_profile(user)

    BooleanSettings.load(user)


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    create_profile(user)
    logger.debug("{} logged in with {}".format(user.email, request))
    # user.profile.set_language(request)

@receiver(password_changed)
def log_password_changed(request, user, **kwargs):
    profile = create_profile(user)
    profile.force_password_change = False
    profile.save()

@receiver(password_reset)
def log_password_reset(request, user, **kwargs):
    profile = create_profile(user)
    profile.force_password_change = False
    profile.save()


 