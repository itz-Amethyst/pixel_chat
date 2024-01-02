from rest_framework import serializers
from .models import Server, Category, Channel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = "__all__"

class ServerSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many = True)

    class Meta:
        model = Server
        exclude = ("member",)

    # Replace num_members with number of members in server
    @staticmethod
    def get_users_count( obj ):
        if hasattr(obj, "users_count"):
            return obj.users_count
        return None

    # Remove the user_count if it was none
    def to_representation(self, instance):
        data = super().to_representation(instance)

        if "users_count" in data and data["users_count"] is None:
            data.pop("users_count")
        
        return data