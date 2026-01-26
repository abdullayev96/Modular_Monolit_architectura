from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=70, min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')


class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True, error_messages={
            'required': 'Email majburiy',
            'invalid': 'To\'g\'ri email kiriting'
        }
    )
    password = serializers.CharField(max_length=128, write_only=True, required=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'Parol majburiy'
        }
    )


class TokenSerializer(serializers.Serializer):
    """Token response serializer."""
    access = serializers.CharField()
    refresh = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    """Success response serializer."""
    data = TokenSerializer()
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    """Error response serializer."""
    message = serializers.CharField()
    errors = serializers.DictField(required=False)
