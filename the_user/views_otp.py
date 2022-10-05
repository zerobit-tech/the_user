from functools import partial

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from the_user.decorators import   change_password_required
 
from django_otp import login 
 
 

from .utils import is_otp_required
from .models import BooleanSettings

from .forms import OTPTokenForm
from .otp_utils import setup_QR_CODE , get_user_totp_device ,delete_user_totp_device

import logging
logger = logging.getLogger('ilogger')

@login_required
@change_password_required
def ask_for_otp(request):
    user = request.user

    next_url = request.GET.get("next", '/')

    # if not is_safe_url(next_url):
    #     next_url = "/"

    if not is_otp_required(user):
        return redirect(next_url)

    form = None
    if request.method == 'POST':
        form = OTPTokenForm(user=user, data=request.POST)
        if form.is_valid():
            login(request, user.otp_device)
            return redirect(next_url)

    else:
        form = OTPTokenForm(user=user, request=request)
    context = {"form": form}

    return render(request, 'the_user/otp.html', context)





@login_required
@change_password_required
def setting_two_factor(request):
    # Profile.objects.all().delete()

    user = request.user
    BooleanSettings.load(user)
    qr_code_url = None
    two_factor_setting = user.booleansettings.get(key=BooleanSettings.AllowedSettings.TWO_FACTOR)

    if request.method == 'POST':
        two_factor = request.POST.get(str(BooleanSettings.AllowedSettings.TWO_FACTOR))
        change2fs = request.POST.get("change2fs")
        if change2fs == "Y":
            message = ""
            if two_factor:
                two_factor_setting.value = True
                device = setup_QR_CODE(user)
                qr_code_url = device.config_url
                message = "Two-factor enabled"
            else:
                two_factor_setting.value = False
                message = "Two-factor disabled"
            two_factor_setting.save()


            if hasattr(request,'capture_user_activity'):
                request.capture_user_activity.send(sender='setting_two_factor', request=request, target=two_factor_setting, message=message)

    if two_factor_setting.value:
        device = setup_QR_CODE(user)
        qr_code_url = device.config_url

    context = {"setting_two_factor": two_factor_setting,
               "qr_code_url": qr_code_url}
    return render(request, 'the_user/setting_two_factor.html', context)


 
# class TOTPVerifyView(views.APIView):
#     """
#     Use this endpoint to verify/enable a TOTP device
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, token, format = None):
#         user = request.user
#         device = get_user_totp_device(self, user)
#         # logger.debug(device, "xx", device.verify_token(token), "QQ", device and device.verify_token(token))
#         if device and device.verify_token(token):
#             if not device.confirmed:
#                 device.confirmed = True
#                 device.save()
#             return Response(True, status=status.HTTP_200_OK)
#
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# class TOTPCreateView(views.APIView):
#     """
#     Use this endpoint to set up a new TOTP device
#     """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, format = None):
#         user = request.user
#         device = setup_QR_CODE(user)
#         url = device.config_url
#         return Response(url, status=status.HTTP_201_CREATED)
