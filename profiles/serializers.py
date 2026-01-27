from rest_framework import serializers
from .models import Profile
from account.models import User
from django.contrib.auth.hashers import make_password
from profiles.service import create_user_profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('full_name', 'number', 'avatar', 'bio', 'balance', 'purchased_book_ids')
        read_only_fields = ('balance', 'purchased_book_ids')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': False},
            'username': {'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        instance.save()
        return instance


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#       class Meta:
#           ref_name = "Profiles"
#           model  = User
#           fields  = ('id', 'email', 'username', 'password')
#           extra_kwargs = {'password': {'write_only': True}}
#
#       def create(self, validated_data):
#           #profile_data = validated_data.pop('profile')
#           password = validated_data.pop('password')
#           user = User(**validated_data)
#           user.set_password(password)
#           user.save()
#
#
#           Profile.objects.create(user=user)
#           return user
#
#       def update(self, instance, validated_data):
#
#           instance.email = validated_data.get('email', instance.email)
#           instance.username = validated_data.get('username', instance.username)
#           #instance.password = validated_data.get('password', instance.password)
#           instance.save()
#
#           return instance