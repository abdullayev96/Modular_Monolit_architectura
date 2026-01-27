from django.shortcuts import render
from .models import Category
from rest_framework.generics import ListCreateAPIView
from .serializers import CategorySerializers
from .services import create_category_logic
from account.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication

#
# class CategoryAPI(ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializers


class CategoryAPI(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        create_category_logic(
            name=validated_data.get('name'),
            slug=validated_data.get('slug')
        )

