from rest_framework import serializers
from .models import Authors


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ('id', 'full_name', "bio", "image")