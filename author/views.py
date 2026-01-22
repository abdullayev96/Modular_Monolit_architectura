from django.shortcuts import render
from .models import Authors
from rest_framework.generics import ListAPIView
from .serializers import AuthorSerializers


class AuthorAPI(ListAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializers
