from .models import Authors
from rest_framework.generics import CreateAPIView
from .serializers import AuthorSerializers
from .services import create_author_logic
from rest_framework.parsers import MultiPartParser, FormParser

# class AuthorAPI(CreateAPIView):
#     queryset = Authors.objects.all()
#     serializer_class = AuthorSerializers


class AuthorAPI(CreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializers

    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        create_author_logic(
            full_name=validated_data.get('full_name'),
            bio=validated_data.get('bio'),
            image=validated_data.get('image')
        )