from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RegisterUserView, LogOutApiView

router = DefaultRouter()
router.register(r'logout', LogOutApiView, basename = "logout")
router.register(r'register', RegisterUserView, basename = "register")
router.register(r'', AccountViewSet, basename = "account")
