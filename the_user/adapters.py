import re
from django.core.exceptions import ValidationError

from allauth.account.adapter import DefaultAccountAdapter

# https://docs.djangoproject.com/en/3.1/topics/auth/passwords/#writing-your-own-validator

# --------------------------------------------------------------
#  Password complexity  password rules  password policy
# --------------------------------------------------------------

class MyAccountAdapter(DefaultAccountAdapter):
    def clean_password(self, password, user=None):
        # TODO --> apply password policy
        return password

        if re.match(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$', password):
            return password
        else:
            raise ValidationError("Error message")

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
        return False