from .models import Authors
from rest_framework.generics import CreateAPIView
from .serializers import AuthorSerializers
from .services import create_author_logic
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from account.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

# class AuthorAPI(CreateAPIView):
#     queryset = Authors.objects.all()
#     serializer_class = AuthorSerializers


class AuthorAPI(CreateAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(operation_id="upload_author_image")  # Swagger-ni majburlash
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


    def perform_create(self, serializer):
        validated_data = serializer.validated_data

        create_author_logic(
            full_name=validated_data.get('full_name'),
            bio=validated_data.get('bio'),
            image=validated_data.get('image')
        )

