import re
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

from allauth.account.adapter import DefaultAccountAdapter
from .utils import _get_setting, is_true
# https://docs.djangoproject.com/en/3.1/topics/auth/passwords/#writing-your-own-validator






# --------------------------------------------------------------
#  Password complexity  password rules  password policy
# --------------------------------------------------------------
class MyAccountAdapter(DefaultAccountAdapter):
    def clean_password(self, password, user=None):
        # TODO --> apply password policy
        
        password_regex = _get_setting("PASSWORD_POLICY_REGEX",None)

        if password_regex is not None:
            if re.match(password_regex, password):
                return password
            else:
                raise ValidationError(_("Password does not satisfy the password policy"))
        
        return password


    def clean_email(self, email):
        """
        Validates an email value. You can hook into this if you want to
        (dynamically) restrict what email addresses can be chosen.
        """
        return email

    # https://django-allauth.readthedocs.io/en/latest/advanced.html#custom-redirects """
    # disable new register
    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        allow_signup = _get_setting("ENABLE_SIGNUP",False)
 
        return True if is_true(allow_signup) else False