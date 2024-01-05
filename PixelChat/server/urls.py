from rest_framework.routers import DefaultRouter
from .views import ServerListViewSet, CategoryListViewSet

router = DefaultRouter()
router.register(r'select', ServerListViewSet)
router.register(r'category', CategoryListViewSet)
