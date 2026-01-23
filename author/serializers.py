from rest_framework import serializers
from .models import Authors


class AuthorSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Authors
        fields = ('full_name', "bio", "image")


