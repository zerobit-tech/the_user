from threading import local
from django.contrib.auth.models import User
from django.conf import settings
 
 
from django.views.i18n import set_language

class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.search_value = request.GET.get('search_value', "").strip()
        
        response = self.get_response(request)
           # Code to be executed for each request/response after
            # the view is called.

        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            lang_code = user.profile.website_language
 
         
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )
        return response


