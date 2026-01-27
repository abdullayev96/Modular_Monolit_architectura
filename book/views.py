from django.shortcuts import render
from .models import Book
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.views import Response
from .serializers import BookSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .services import create_book_logic
from .services import enrich_books_data
from drf_spectacular.utils import extend_schema
from account.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

# class BookAPI(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class BookListAPI(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]


    parser_classes = (MultiPartParser, FormParser)


    @extend_schema(
        request={
            'multipart/form-data': BookSerializer
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # Ma'lumotlarni yig'ish (N+1 muammosiz)
        queryset = self.get_queryset()
        books = list(queryset)
        enriched_books = enrich_books_data(books)

        serializer = self.get_serializer(enriched_books, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            create_book_logic(**serializer.validated_data)
        except Exception as e:
            print(f"Xatolik: {e}")
            raise serializers.ValidationError({"detail": str(e)})

