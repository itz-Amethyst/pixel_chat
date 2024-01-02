from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):

    # Implement user profile picture later and model
    class Meta:
        model = Account
        fields = ("username",)