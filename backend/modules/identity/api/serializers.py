from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from modules.identity.models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=191)
    username = serializers.RegexField(
        r"^[A-Za-z0-9_]{3,30}$",
        error_messages={"invalid": "Use 3-30 letters, numbers or underscores."},
    )
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(max_length=120, required=False, allow_blank=True)

    def validate(self, data):
        candidate = User(email=data["email"], username=data["username"])
        validate_password(data["password"], user=candidate)
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=100)


class ResetPasswordSerializer(TokenSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="role.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "headline",
            "bio",
            "country",
            "avatar_url",
            "role",
            "is_email_verified",
            "show_on_leaderboard",
            "created_at",
        ]
        read_only_fields = fields


class ProfileUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
    headline = serializers.CharField(max_length=160, required=False, allow_blank=True)
    bio = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    country = serializers.RegexField(r"^([A-Z]{2})?$", required=False, allow_blank=True)
    show_on_leaderboard = serializers.BooleanField(required=False)
