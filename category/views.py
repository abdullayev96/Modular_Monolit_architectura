from django.shortcuts import render
from .models import Category
from rest_framework.generics import ListCreateAPIView
from .serializers import CategorySerializers
from .services import create_category_logic

#
# class CategoryAPI(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializers


class CategoryAPI(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        create_category_logic(
            name=validated_data.get('name'),
            slug=validated_data.get('slug')
        )

