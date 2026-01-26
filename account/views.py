from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import *
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .services import register_user_logic

import logging
logger = logging.getLogger(__name__)
from drf_spectacular.utils import extend_schema, OpenApiResponse


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("api_requests.log"),
        logging.StreamHandler()
    ]
)


class RegisterAPI(APIView):
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="Yangi foydalanuvchini ro'yxatdan o'tkazish",
        request=RegisterSerializer,
        responses={201: RegisterSerializer}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Barcha mantiq (User + Profile yaratish) servisda
            user = register_user_logic(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            return Response({
                "msg": "Muvaffaqiyatli ro'yxatdan o'tdingiz!",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Xatolikni konsolda ko'rish uchun
            print(f"Registration Error: {e}")
            return Response(
                {"error": "Tizimda xatolik yuz berdi"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


@extend_schema(
    request=LoginSerializers,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='Muvaffaqiyatli login'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Validatsiya xatosi'
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Noto\'g\'ri email yoki parol'
        ),
        403: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Foydalanuvchi aktiv emas'
        ),
    },
    summary='User login',
    description='Staff foydalanuvchilar uchun login endpoint',
    tags=['Authentication'])


class LoginAPI(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # Validatsiya
        if not serializer.is_valid():
            return Response(
                {
                    'message': 'Validatsiya xatosi',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {'message': 'Email yoki parol noto\'g\'ri'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # is_active check
        if not user.is_active:
            return Response(
                {'message': 'Sizning akkauntingiz faol emas'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            tokens = self._get_tokens_for_user(user)
            logger.info(f'User logged in: {email}')

            return Response(
                {
                    'data': tokens,
                    'message': 'Muvaffaqiyatli login'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Token generation error: {str(e)}', exc_info=True)
            return Response(
                {'message': 'Token yaratishda xatolik'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def _get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        }
