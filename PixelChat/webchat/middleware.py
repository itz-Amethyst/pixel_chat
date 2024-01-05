import jwt
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(scope):

    token = scope["token"]
    model = get_user_model()

    try:
        if token:
            user_id = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.JWT_ALGORITHM])["user_id"]
            return model.objects.get(id = user_id)
        else:
            return AnonymousUser()
    except (jwt.exceptions.DecodeError, model.DoesNotExist):
        return AnonymousUser()

# Remember to config it in asgi Main app
class JWTAuthMiddleWare:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers_dict = dict(scope["headers"])
        cookie_str = headers_dict.get(b"cookie", "").decode()
        cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookie_str.split("; ")}
        access_token = cookies.get("access_token")

        # Fill the datas
        scope["token"] = access_token
        scope["user"] = await get_user(scope)

        return await self.app(scope, receive, send)