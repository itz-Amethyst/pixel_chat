from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializer import ServerSerializer , CategorySerializer
from .schema import server_list_docs

from .models import Server, Category

# class ServerMembershipViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request, server_id):
#         pass
#
#     def destroy(self, request, server_id):
#         pass


class CategoryListViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses = CategorySerializer)
    def list( self, request ):
        serializer = CategorySerializer(self.queryset, many = True)
        return serializer.data



class ServerListViewSet(viewsets.ViewSet):
    # use chatgpt later for docstring command: => build doc string in google style <code>

    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """Get a list of servers based on specified query parameters.

        - `category` (str, optional): Category of servers to retrieve.
        - `current_user` (bool, optional): Filter servers for the current user.
        - `take` (int, optional): Limit the number of servers to retrieve.
        - `server_id` (int, optional): ID of the server to retrieve.
        - `members_count` (bool, optional): Include the count of members for each server.

        Returns:
            Response: The serialized list of servers.

        Raises:

        `AuthenticationFailed`:
            If 'current_user' is True, but the user is not authenticated.

        `ValidationError`:
            If 'server_id' is provided, but the server with that ID does not exist.
        """

        category = request.query_params.get("category")
        only_logged_user = request.query_params.get("current_user") == "true"
        count = request.query_params.get("take")
        server_id = request.query_params.get("server_id")
        members_count = request.query_params.get("members_count") == "true"

        if members_count:
            self.queryset = self.queryset.annotate(users_count=Count("member"))

        if category:
            if not self.queryset.filter(category__name=category).exists():
                raise ValidationError(detail=f"Server with category of {category} does not exists.")
            self.queryset = self.queryset.filter(category__name=category)

        if only_logged_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        # can add authentication logic here
        if server_id:
            if not self.queryset.filter(id=server_id).exists():
                raise ValidationError(
                    detail=f"Server with id {server_id} does not exists."
                )
            self.queryset = self.queryset.filter(id=server_id)

        if count:
            self.queryset = self.queryset[:int(count)]

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
