from django.shortcuts import render
from .models import Book
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import Response
from .serializers import BookSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .services import create_book_logic
from .services import enrich_books_data
from rest_framework import serializers
# class BookAPI(ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class BookListAPI(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        # Ma'lumotlarni yig'ish (N+1 muammosiz)
        queryset = self.get_queryset()
        books = list(queryset)
        enriched_books = enrich_books_data(books)

        serializer = self.get_serializer(enriched_books, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # POST so'rovi shu yerda ishlaydi
        try:
            create_book_logic(**serializer.validated_data)
        except ValueError as e:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"detail": str(e)})