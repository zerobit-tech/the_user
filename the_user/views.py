from django.shortcuts import render,redirect

from .forms import UserForm, UserProfileForm
from .models import BooleanSettings
# Create your views here.
from django.contrib.auth.decorators import login_required
from the_user.decorators import otp_required, must_be, change_password_required


from the_user.utils import user_is
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER

import logging
logger = logging.getLogger('ilogger')

@login_required
@otp_required
@change_password_required
def setting(request):
    # Profile.objects.all().delete()
    user = request.user
    user_form = UserForm()
    profile_form = UserProfileForm()

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            profile_data = profile_form.cleaned_data
           # user.username = user_data['username']
            user.email = user_data['email']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            # user.profile.home_phone_number = profile_data['home_phone_number']
            user.save()

            user.profile.website_language = profile_data['website_language']
            user.profile.communication_language = profile_data['communication_language']
            user.profile.save()
            # TODO --> send message on save sucessful

            # user = user_form.save()
            # profile = profile_form.save(commit=False)
            # profile.user = user
            # profile.save()
    else:
        # user_form.fields["username"].initial = user.username
        user_form.fields["email"].initial = user.email
        user_form.fields["first_name"].initial = user.first_name
        user_form.fields["last_name"].initial = user.last_name
        profile_form.fields["website_language"].initial = user.profile.website_language
        profile_form.fields["communication_language"].initial = user.profile.communication_language

        # profile_form.fields["home_phone_number"].initial = user.profile.home_phone_number

    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request, 'the_user/settings.html', context)

# -------------------------------------------------


#
# @login_required
# def verify(request):
#     form_cls = partial(OTPTokenForm, request.user)
#
#     return LoginView.as_view(request, template_name='account/otp.html', authentication_form=form_cls)


@login_required
@otp_required
@change_password_required
def landing_page(request):
    # TODO: where to land user on login
    from the_user.decorators import otp_required, _internal_dashboard,_external_dashboard

    print("_internal_dashboard",_internal_dashboard)
    if user_is(request.user, CUSTOMER_CARE_REP  ):
        if _internal_dashboard:
            return _internal_dashboard(request)
        else:
            return  redirect("the_user:settings")
     
    else:
        if _external_dashboard:
            return _external_dashboard(request)
        else:    
            return  redirect("the_user:settings")
        #return redirect("creditline_customer_base:accounts",customer_id=request.user.customer.uuid)