from django.contrib.auth.decorators import user_passes_test

from django_otp import user_has_device
from django_otp.conf import settings
from .models import BooleanSettings
from .utils import is_otp_required,user_is,need_to_change_password
from functools import wraps

from django.core.exceptions import PermissionDenied


import logging
logger = logging.getLogger('ilogger')

# ---------------------------------------------------------------
# 
# ---------------------------------------------------------------
_internal_dashboard=None
_external_dashboard=None


def internal_dashboard(func):
    global _internal_dashboard
    _internal_dashboard = func

    @wraps(func)
    def actual_decorator(*args, **kwargs):
        value = func(*args, **kwargs)
        return value

    return actual_decorator

# ---------------------------------------------------------------
def external_dashboard(func):
    global _external_dashboard
    _external_dashboard = func

    @wraps(func)
    def actual_decorator(*args, **kwargs):
        value = func(*args, **kwargs)
        return value

    return actual_decorator 
# ---------------------------------------------------------------
# 
# ---------------------------------------------------------------

_auth_methods = []

def register_auth_method(func):
    global _auth_methods
    if func not in _auth_methods:
        _auth_methods.append(func)

    @wraps(func)
    def actual_decorator(*args, **kwargs):
        value = func(*args, **kwargs)
        return value

    return actual_decorator
        

# ---------------------------------------------------------------
#
# ---------------------------------------------------------------

# def is_customer_care_rep(view = None, redirect_field_name = 'next', login_url = None, if_configured = False):

#     def test(user):
#         return not is_in_group(user,CUSTOMER_CARE_REP)

#     decorator = user_passes_test(test, login_url=login_url, redirect_field_name=redirect_field_name)

#     return decorator if (view is None) else decorator(view)

# ---------------------------------------------------------------
#
# ---------------------------------------------------------------

def must_be(group_name):
    def actual_decorator(view_function):
        @wraps(view_function)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            #logger.debug("request.user >> ", request.user)
            if user_is(user,group_name):
                return view_function(request, *args, **kwargs)
            else:
                raise PermissionDenied()

        return _wrapped_view

    
    return actual_decorator

# ---------------------------------------------------------------
#
# ---------------------------------------------------------------

def otp_required(view_function = None, redirect_field_name = 'next', login_url = None, if_configured = False):
    """
    Similar to :func:`~django.contrib.auth.decorators.login_required`, but
    requires the user to be :term:`verified`. By default, this redirects users
    to :setting:`OTP_LOGIN_URL`.


    """
    if login_url is None:
        login_url = settings.OTP_ENTRY_URL

    # if fails go to login/otp url
    def test(user):
        return not is_otp_required(user)

        # two_factor_enabled = user.booleansettings.get(key=BooleanSettings.AllowedSettings.TWO_FACTOR)
        # if not two_factor_enabled:
        #     return True
        #
        # if not user_has_device(user):
        #     return True
        #
        # if user.is_verified():
        #     return True
        # return False

    decorator = user_passes_test(test, login_url=login_url, redirect_field_name=redirect_field_name)

    return decorator if (view_function is None) else decorator(view_function)

    #
    # def my_login_required(view_function, redirect_field_name = 'next', login_url = None, ):
    #     @functools.wraps(view_function)
    #     def check_user(request, *args, **kwargs):
    #         user = request.user
    #         two_factor_enabled = False
    #         login_url = None
    #         user_test = None
    #
    #         if not user.is_authenticated:  # go to login url
    #             path = request.build_absolute_uri()
    #             resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
    #             # If the login url is the same scheme and net location then just
    #             # use the path as the "next" url.
    #             login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    #             current_scheme, current_netloc = urlparse(path)[:2]
    #             if ((not login_scheme or login_scheme == current_scheme) and
    #                     (not login_netloc or login_netloc == current_netloc)):
    #                 path = request.get_full_path()
    #             from django.contrib.auth.views import redirect_to_login
    #             return redirect_to_login(
    #                 path, resolved_login_url, redirect_field_name)
    #
    #         if user.is_authenticated:
    #             two_factor_enabled = user.booleansettings.get(key=BooleanSettings.AllowedSettings.TWO_FACTOR)
    #
    #         '''
    #           two-factor is enabled
    #           user has a device attached
    #
    #           and
    #
    #           user is_authenticated  but not verified yet
    #
    #         '''
    #         if (two_factor_enabled and user_has_device(user)) and (user.is_authenticated and not user.is_verified()):
    #             login_url = settings.OTP_ENTRY_URL
    #             path = request.build_absolute_uri()
    #             resolved_login_url = resolve_url(login_url or settings.OTP_ENTRY_URL)
    #             # If the login url is the same scheme and net location then just
    #             # use the path as the "next" url.
    #             login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
    #             current_scheme, current_netloc = urlparse(path)[:2]
    #             if ((not login_scheme or login_scheme == current_scheme) and
    #                     (not login_netloc or login_netloc == current_netloc)):
    #                 path = request.get_full_path()
    #             from django.contrib.auth.views import redirect_to_login
    #             return redirect_to_login(
    #                 path, resolved_login_url, redirect_field_name)
    #
    #         return view_function(request, *args, **kwargs)
    #
    #     return check_user

    '''
      who do we know if user has been verified or not?
      def is_verified(user):
            return user.otp_device is not None
      
      
        Django-otp middleware(OTPMiddleware) checks DEVICE_ID_SESSION_KEY = 'otp_device_id' in the session
        
            >> it sets   _verify_user > user.otp_device = None  <<<<<<<<<<<<<<<<<< 1
        
      there is a signal attached
          user_logged_in.connect(_handle_auth_login)  
          
          it checks hasattr(user, 'otp_device'): >> if user is enrolled for OTP
          
          
       user submits "OTPTokenForm" which use OTPAuthenticationFormMixin
            which call _verify_token()
            
    
        user.otp_device = self._verify_token(user, token, device) <<<<<<<<<<<< 2
           
      
    '''


# ---------------------------------------------------------------
#
# ---------------------------------------------------------------

def change_password_required(view_function = None, redirect_field_name = 'next', login_url = None, if_configured = False):
    """
    Similar to :func:`~django.contrib.auth.decorators.login_required`, but
    requires the user to be :term:`verified`. By default, this redirects users
    to :setting:`OTP_LOGIN_URL`.


    """
    if login_url is None:
        from django.urls import reverse_lazy

        login_url = reverse_lazy('account_change_password')

    # if fails go to login/otp url
    def test(user):
        return not need_to_change_password(user)
 

    decorator = user_passes_test(test, login_url=login_url, redirect_field_name=redirect_field_name)

    return decorator if (view_function is None) else decorator(view_function)