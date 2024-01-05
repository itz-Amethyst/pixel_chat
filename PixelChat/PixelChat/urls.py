from django.contrib import admin
from django.urls import path , include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

import account.urls
import server.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view()),

    #! Main
    path('api/server/', include(server.urls.router.urls)),

    #? Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #? Account
    path('api/account/', include(account.urls.router.urls)),
]

websocket_urlpatterns = [path("<str:serverId>")]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
