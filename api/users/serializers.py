from rest_framework import serializers

from api.core.serialize_fields.email import LowercaseEmailField
from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    email = LowercaseEmailField(
        required=False, allow_null=True, write_only=True
    )
    first_name = serializers.CharField(required=False, max_length=200, allow_null=True)
    last_name = serializers.CharField(required=False, max_length=200, allow_null=True)
    type_user = serializers.CharField(max_length=2)
    password = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "type_user",
            "password",
            "username",
        )
