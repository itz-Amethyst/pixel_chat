from django.contrib.auth import get_user_model
from django.db import models

from server.models import Channel


# Create your models here.
class Conversation(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete = models.CASCADE, blank = False, null = False)
    created_at = models.DateTimeField(auto_now_add = True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete = models.CASCADE, related_name = "message")
    sender = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"by: {self.sender} , {self.content} , {self.timestamp.date()}"