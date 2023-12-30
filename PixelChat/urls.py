from django.contrib import admin
from django.urls import path , include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

import server.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view()),

    path('api/server/', include(server.urls.router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
