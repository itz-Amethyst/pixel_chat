from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer


server_list_docs = extend_schema(
    responses = ServerSerializer(many = True),
    parameters = [
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of servers to retrieve.",
        ),
        OpenApiParameter(
            name="current_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter servers for the current user.",
        ),
        OpenApiParameter(
            name="take",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Limit the number of servers to retrieve.",
        ),
        OpenApiParameter(
            name="server_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="ID of the server to retrieve.",
        ),
        OpenApiParameter(
            name="members_count",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the count of members for each server.",
        ),
    ],
)