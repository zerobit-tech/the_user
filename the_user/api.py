 
from django.urls import reverse_lazy
from ninja import Router 
from ninja.security import django_auth
 
from django_otp import login, devices_for_user

from ninja import Schema , Field
from .otp_utils import get_user_totp_device, delete_user_totp_device
from the_user.api_auth import BearerAuth 


router = Router(auth= BearerAuth())
internal_router = Router(auth=django_auth) 
 

# -------------------------------------------------------
#
# -------------------------------------------------------

class TokenSchema(Schema):
    token:str 
 

@internal_router.post("/verify2ft", url_name="setting_two_factor_verification")
def verify2ft(request, token:TokenSchema):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    token_to_check = token.dict().get("token",None)
    user = request.user
    device = get_user_totp_device(user)
    if device and device.verify_token(token_to_check):
            if not device.confirmed:
                device.confirmed = True
                device.save()

                # auto login user >> on verification
            login(request, device)
            #logger.debug("request.session[DEVICE_ID_SESSION_KEY]>>>", request.session['otp_device_id'])

            return 200 ,{"verified": True}

    return   200 ,{"verified": False}



class ResetSchema(Schema):
    reset:bool 

@internal_router.post("/reset2ft", url_name="setting_two_factor_reset")
def reset2ft(request, data:ResetSchema):
        reset = data.dict()["reset"]
        if reset:
            user = request.user
            delete_user_totp_device(user)

        return 200, {"done": True}