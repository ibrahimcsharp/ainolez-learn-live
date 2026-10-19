from rest_framework import serializers, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from modules.media import services
from modules.media.models import MediaFile
from shared.admin_api import AdminResourceViewSet


class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = [
            "id",
            "url",
            "original_name",
            "mime_type",
            "size_bytes",
            "width",
            "height",
            "alt_text",
            "is_active",
            "created_at",
            "deleted_at",
        ]
        read_only_fields = [f for f in fields if f != "alt_text"]


class MediaFileViewSet(AdminResourceViewSet):
    model = MediaFile
    serializer_class = MediaFileSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    search_fields = ("original_name", "alt_text")
    filter_fields = ("mime_type",)

    def create(self, request, *args, **kwargs):
        upload = request.FILES.get("file")
        if upload is None:
            return Response({"file": ["Choose a file."]}, status=status.HTTP_400_BAD_REQUEST)
        media = services.upload(upload, request.data.get("alt_text", ""), request.user)
        return Response(self.get_serializer(media).data, status=status.HTTP_201_CREATED)
