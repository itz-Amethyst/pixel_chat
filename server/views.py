from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializer import ServerSerializer

from .models import Server


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()
    def list(self, request):
        category = request.query_params.get("category")
        only_logged_user = request.query_params.get("current_user") == "true"
        count = request.query_params.get("take")

        if category:
            self.queryset = self.queryset.filter(category__name = category)

        if only_logged_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member = user_id)

        if count:
            self.queryset = self.queryset.filter[:int(count)]

        serializer = ServerSerializer(self.queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)