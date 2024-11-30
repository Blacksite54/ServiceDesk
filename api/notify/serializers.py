from rest_framework import serializers

from api.notify.models import NotifyUser


class NotifyUserSerializer(serializers.ModelSerializer):
    is_view = serializers.BooleanField()

    class Meta:
        model = NotifyUser
        fields = (
            "id",
            "message",
            "is_view",
            "created_at",
        )
        read_only_fields = (
            "id",
            "message",
            "created_at",
        )

    def update(self, instance, validated_data):
        instance.is_view = validated_data.get("is_view", instance.is_view)
        instance.save()

        return instance