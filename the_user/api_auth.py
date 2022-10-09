
from webbrowser import get
from ninja.security import HttpBearer
import logging
logger = logging.getLogger('ilogger')


class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        from .decorators import _auth_methods
        autherized = None
        for auth_method in _auth_methods:
            # call each method if any return not None --> authoerized
            autherized = auth_method(request, token)
            logger.debug(f"auth method {auth_method} : {autherized}")

            if autherized:
                break
        logger.debug(f"BearerAuth final response: {autherized}")     
        return autherized  # unauthoerized 
 