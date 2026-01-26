from rest_framework import serializers
from .models import Book
from drf_spectacular.utils import extend_schema_field


class BookSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=False, allow_null=True)
    author_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'title', 'image', 'price', 'author_id', 'category_id', 'author_name', 'category_name')


    @extend_schema_field(serializers.CharField())
    def get_author_name(self, obj):
        # Agar View ma'lumotni boyitgan bo'lsa, o'shani qaytaradi
        return getattr(obj, 'author_name', "Noma'lum")

    @extend_schema_field(serializers.CharField())
    def get_category_name(self, obj):
        return getattr(obj, 'category_name', "Ma'lumot yo'q")