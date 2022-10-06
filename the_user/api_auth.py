
from webbrowser import get
from ninja.security import HttpBearer
from .decorators import _auth_methods


class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        autherized = None
        for auth_method in _auth_methods:
            # call each method if any return not None --> authoerized
            autherized = auth_method(request, token)
            if autherized:
                break
        return autherized  # unauthoerized 
 