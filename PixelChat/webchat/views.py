from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status

from rest_framework.response import Response

from .schemas import list_message_docs
from .models import Conversation
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ViewSet):

    @list_message_docs
    def list( self, request ):
        channel_id = request.query_params.get("channel_id")

        try:
            conversation = get_object_or_404(Conversation, channel_id = channel_id)
            message = conversation.message.all()
            serializer = MessageSerializer(message, many = True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(data = [], status = status.HTTP_404_NOT_FOUND)
