from django.conf import settings
from rest_framework import viewsets , status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView

from .models import Account
from .schemas import user_list_docs
from .serializers import AccountSerializer , RegisterSerializer , JWTCookieTokenRefreshSerializer , \
    CustomTokenObtainPairSerializer


class RegisterUserView(APIView):
    def post( self, request ):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]

            # Prevent create action by these names
            forbidden_name = ["admin", "root", "superuser", "milad"]
            if username is forbidden_name:
                return Response({"error:": f"Username {username} not allowed!"}, status = status.HTTP_409_CONFLICT)

            serializer.save()
            return Response({"success": f"User {username} successfully created"}, status = status.HTTP_200_OK)

        errors = serializer.errors
        if "username" in errors and "non_field_errors" not in errors:
            return Response({"error:": errors["username"][0]})

        return Response(errors, status = status.HTTP_400_BAD_REQUEST)



class LogOutApiView(APIView):

    @staticmethod
    def post( self, request ):
        # Todo get use name from request , print in response
        response = Response("Logged Out Successfully!")
        response.set_cookie("refresh_token", "", expires = 0)
        response.set_cookie("access_token", "", expires = 0)
        return response


class AccountViewSet(viewsets.ViewSet):

    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]

    @user_list_docs
    def list( self, request ):
        user_id = request.query_params.get("user_id")
        queryset = Account.objects.get(id = user_id)
        serializer = AccountSerializer(queryset)
        return Response(serializer.data)



class JWTSetCookieMixIn:
    def finalize_response(self, request, response: Response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                httponly = True,
                max_age = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                samesite = settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"]
            )

        if response.data.get("access"):
            response.set_cookie(
                settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                httponly = True,
                max_age = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                samesite = settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"]
            )

            del response.data["access"]

        return super().finalize_response(request, response, *args, **kwargs)


class JWTCookieTokenObtainPerView(JWTSetCookieMixIn, TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class JWTCookieRefreshTokenView(JWTSetCookieMixIn, TokenRefreshView):
    serializer_class = JWTCookieTokenRefreshSerializer