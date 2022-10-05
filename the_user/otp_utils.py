
from django_otp import login, devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.conf import settings
from django_otp.util import random_hex


def delete_user_totp_device(user, confirmed = None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        device.delete()


def get_user_totp_device(user, confirmed = None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


def setup_QR_CODE(user):
    key = random_hex(length=35)
    device = get_user_totp_device(user)
    if not device:
        device = user.totpdevice_set.create(confirmed=False,
                                            name="{}:{}".format(settings.OTP_TOTP_ISSUER, user.username), key=key)
    return device