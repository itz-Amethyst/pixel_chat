from django.contrib import admin
from django.urls import path , include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

import server.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/schema', SpectacularAPIView.as_view(), name="schema"),
    path('api/docs/', SpectacularSwaggerView.as_view()),

    path('api/server/', include(server.urls.router.urls))
]
