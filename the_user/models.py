from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
 
from django.utils import translation 

import logging
logger = logging.getLogger('ilogger')
# Create your models here.
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                     "allowed.")


# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,verbose_name=_("User"),
                                related_name="profile",
                                primary_key=True)

    website_language = models.CharField(max_length=2, choices=settings.LANGUAGES, default='en')
    communication_language = models.CharField(max_length=2, choices=settings.LANGUAGES, default='en')

    force_password_change = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


    #----------------------------------------------------------------
    def get_change_password_url(self):
        from django.urls import reverse
        return reverse('account_change_password')

    # def set_language(self,request):
    #     translation.activate(self.language) 

    #     request.session[LANGUAGE_SESSION_KEY] = self.language
    #     request.session.save()
# # --------------------------------------------------------------------------------
# #
# # --------------------------------------------------------------------------------
# class Address(models.Model):
#     class Types(models.TextChoices):
#         HOME = 'H', _('Home')
#         SHIPPING = 'S', _('Shipping')
#         OFFICE = 'O', _('Office')
#         BILLING = 'B', _('Billing')
#
#
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
#     # profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='addresses')
#
#     type = models.CharField(max_length=1, choices=Types.choices, default=Types.HOME)
#     address1 = models.CharField(max_length=50)
#     address2 = models.CharField(max_length=50, blank=True)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     postcode = models.CharField(max_length=10)
#     country = models.CharField(max_length=3, choices=ISO_3166_CODES)
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)
#     def clean(self):
#         # Ensure postcodes are valid for country
#         self.ensure_postcode_is_valid_for_country()
#
#     def ensure_postcode_is_valid_for_country(self):
#         """
#         Validate postcode given the country
#         """
#
#
#         if self.postcode and self.country:
#             # Ensure postcodes are always uppercase
#             postcode = self.postcode.upper().replace(' ', '')
#
#             regex = self.POSTCODES_REGEX.get(self.country, None)
#
#             # Validate postcode against regex for the country if available
#             if regex and not re.match(regex, postcode):
#                 msg = _("The postcode '%(postcode)s' is not valid "
#                         "for %(country)s") \
#                       % {'postcode': self.postcode,
#                          'country': self.country}
#                 raise exceptions.ValidationError(
#                     {'postcode': [msg]})
#
#     def __str__(self):
#         return '{}:{}'.format(Address.Types(self.type).label, self.address1)
# --------------------------------------------------------------------------------
#
# --------------------------------------------------------------------------------

class BooleanSettings(models.Model):
    class AllowedSettings(models.TextChoices):
        TWO_FACTOR = 'TWO_FACTOR', _('Enable Two-Factor authentication?')
        GENERATE_INVOICE = 'GENERATE_INVOICE', _('Generate invoice for each Transaction?')

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="booleansettings",
                             null=False, blank=False, verbose_name=_("User")
                             )
    key = models.CharField(max_length=50, choices=AllowedSettings.choices, null=False, blank=False,
                           verbose_name="Setting")
    value = models.BooleanField(verbose_name="Enabled", default=False, blank=False, null=False )

    class Meta:
        ordering = ['user', 'key']
        constraints = [
            models.UniqueConstraint(fields=['user', 'key'], name='User unique Setting')
        ]

    def __str__(self):
        return self.key;

    @staticmethod
    def load(user):
        for setting in BooleanSettings.AllowedSettings:
            boolean_setting = BooleanSettings.objects.filter(user=user).filter(key=setting).first()
            if not boolean_setting:
                boolean_setting = BooleanSettings(user=user, key=setting)
                boolean_setting.save()


