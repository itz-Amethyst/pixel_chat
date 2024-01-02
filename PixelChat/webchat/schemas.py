from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from webchat.serializers import MessageSerializer

list_message_docs = extend_schema(
    responses = MessageSerializer(many = True),
    parameters = [
        OpenApiParameter(
            name = "channel_id",
            location = OpenApiParameter.QUERY,
            type = OpenApiTypes.STR,
            description = "ID of channel"
        )
    ]
)