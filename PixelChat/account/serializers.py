from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):

    # Implement user profile picture later and model
    class Meta:
        model = Account
        fields = ("username",)

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ("username", "password",)

    # To check If user exists
    def is_valid( self, raise_exception = False):
        valid = super().is_valid(raise_exception = raise_exception)

        if valid:
            username = self.validated_data["username"]
            if Account.objects.exists(username = username):
                self._errors["username"] = [f"Username: {username} exists."]
                valid = False

        return valid

    def create(self, validated_data):
        user = Account.objects.create(**validated_data)
        return user
