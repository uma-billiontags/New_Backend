from rest_framework import serializers
from .models import Lead, LeadAttachment, LeadCategory   


class LeadAttachmentSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = LeadAttachment
        fields = ["id", "filename", "mime_type", "size", "download_url"]

    def get_download_url(self, obj):
        request = self.context.get("request")
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url


# ── NEW ──
class LeadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadCategory
        fields = ["id", "name"]


class LeadSerializer(serializers.ModelSerializer):
    attachments = LeadAttachmentSerializer(many=True, read_only=True)
    client_id = serializers.CharField(source="client.client_id", read_only=True, default=None)

    class Meta:
        model = Lead
        fields = [
            "id", "sender", "receiver", "subject", "body",
            "thread_id", "message_id", "mail_link",
            "received_at", "created_at",
            "category_status", "category_name",
            "ticket_id", "client", "client_id",
            "attachments",
        ]