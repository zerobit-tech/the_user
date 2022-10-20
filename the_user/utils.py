from django_otp import user_has_device
from django.conf import settings

from .models import BooleanSettings
from .initial_groups import GROUP_WEIGHTAGE


def _get_setting(key, default):
    return_value =  getattr(settings, key, default)
    if return_value is None:
        return_value = default
    return return_value

def is_true(v):
    if isinstance(v, bool):
        return v

    return v.lower() in ("yes", "true", "t", "1",)



def is_otp_required(user):
    two_factor_enabled = user.booleansettings.get(key=BooleanSettings.AllowedSettings.TWO_FACTOR)
    if not two_factor_enabled.value:
        return False

    if not user_has_device(user):
        return False

    if user.is_verified():
        return False

    return True

def need_to_change_password(user):
    return user.profile.force_password_change



def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def is_in_multiple_groups(user, groups):
    return user.groups.filter(name__in=groups).exists()



def user_is(user, group_name):
    if user.is_superuser:
        return True

    if not user.is_staff:
        return False

    groups_to_check = {group_name,}
    min_group_weight = GROUP_WEIGHTAGE.get(group_name,0)
    for group_name in GROUP_WEIGHTAGE.keys():
        group_weight = GROUP_WEIGHTAGE.get(group_name,0)
        if group_weight>=min_group_weight:
            groups_to_check.add(group_name)

    return is_in_multiple_groups(user=user, groups=list(groups_to_check))

    

