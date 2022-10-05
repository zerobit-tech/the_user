from django import forms

from django_otp.forms import OTPAuthenticationFormMixin

from django.conf import settings

from .models import Profile
from django.contrib.auth.models import User

import logging
logger = logging.getLogger('ilogger')
# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["website_language","communication_language"]



# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class OTPTokenForm(OTPAuthenticationFormMixin, forms.Form):
    """
         copy from django_otp.forms.OTPTokenForm

    """
    otp_device = forms.ChoiceField(choices=[], label="Token Type")
    otp_token = forms.CharField(required=True, label="Token", widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    def __init__(self, user, request = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        self.fields['otp_device'].choices = self.device_choices(user)

    def clean(self):
        super().clean()

        self.clean_otp(self.user)

        return self.cleaned_data

    def get_user(self):
        return self.user
