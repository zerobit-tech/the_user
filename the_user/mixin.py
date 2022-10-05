from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER, ADMIN
from the_user.decorators import otp_required, must_be, change_password_required
 
# --------------------------------------------------------------
#
# --------------------------------------------------------------
class OPTRequiredMixin(AccessMixin):
    @method_decorator(login_required)
    @method_decorator(otp_required)
    @method_decorator(change_password_required)
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)


# --------------------------------------------------------------
#
# --------------------------------------------------------------
class AdminRequiredMixin(AccessMixin):
    @method_decorator(login_required)
    @method_decorator(otp_required)
    @method_decorator(change_password_required)
    @method_decorator(must_be(group_name=ADMIN))
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)

# --------------------------------------------------------------
#
# --------------------------------------------------------------   
class CCSRequiredMixin(AccessMixin):
    @method_decorator(login_required)
    @method_decorator(otp_required)
    @method_decorator(change_password_required)
    @method_decorator(must_be(group_name=CUSTOMER_CARE_SUPERVISER))
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)

# --------------------------------------------------------------
#
# --------------------------------------------------------------
class CCRRequiredMixin(AccessMixin):
    @method_decorator(login_required)
    @method_decorator(otp_required)
    @method_decorator(change_password_required)
    @method_decorator(must_be(group_name=CUSTOMER_CARE_REP))
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)
    
# --------------------------------------------------------------
#
# --------------------------------------------------------------
class CCMRequiredMixin(AccessMixin):
    @method_decorator(login_required)
    @method_decorator(otp_required)
    @method_decorator(change_password_required)
    @method_decorator(must_be(group_name=CUSTOMER_CARE_MANAGER))
    def dispatch(self, request , *args , **kwargs ) :
        return super().dispatch(request, *args, **kwargs)