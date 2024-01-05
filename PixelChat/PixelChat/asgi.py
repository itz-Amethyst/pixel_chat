"""
ASGI config for PixelChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Custom
from channels.routing import ProtocolTypeRouter, URLRouter
from . import urls
from webchat.middleware import JWTAuthMiddleWare

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PixelChat.settings')

django_application = get_asgi_application()


application = ProtocolTypeRouter(
    {
        # Todo: check get_asgi_application
        "http": django_application,
        "websocket": JWTAuthMiddleWare(URLRouter(urls.websocket_urlpatterns))

    }
)