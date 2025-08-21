from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class NotificationSerializer(serializers.ModelSerializer):
    recipient = SimpleUserSerializer(read_only=True)
    actor = SimpleUserSerializer(read_only=True)
    verb = serializers.CharField()
    target_type = serializers.SerializerMethodField()
    target_id = serializers.IntegerField(source="target_object_id")
    timestamp = serializers.DateTimeField(read_only=True)
    read = serializers.BooleanField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor",
            "verb",
            "target_type",
            "target_id",
            "timestamp",
            "read",
        ]

    def get_target_type(self, obj):
        return obj.target_content_type.model if obj.target_content_type else None
