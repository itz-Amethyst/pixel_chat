from typing import Optional , Tuple

from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication , AuthUser
from rest_framework_simplejwt.tokens import Token


class JWTCookieAuthentication(JWTAuthentication):

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:

        raw_token = request.COOKIES.get(settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"]) or None

        if raw_token is None:
            return None

        validation_token = self.get_validated_token(raw_token)
        # Return User Info and Encoded Token
        return self.get_user(validation_token), validation_token
