from rest_framework import serializers
from .models import Profile
from account.models import User
from django.contrib.auth.hashers import make_password
from profiles.service import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'username': {'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # Email va usernameni yangilash
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        if password:
            instance.set_password(password)  # Parolni hash qilish

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('full_name', 'number', 'avatar', 'bio', 'balance', 'purchased_book_ids')
        read_only_fields = ('balance', 'purchased_book_ids')