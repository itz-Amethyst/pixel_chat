from rest_framework.routers import DefaultRouter
from .views import ServerListViewSet, CategoryListViewSet, ServerMembershipViewSet

router = DefaultRouter()
router.register(r'select', ServerListViewSet)
router.register(r'category', CategoryListViewSet)
router.register(r'membership/(?P<server_id>\d+)/membership', ServerMembershipViewSet, basename = "server-membership")
