from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from .service import ProfileService


class ProfileAPI(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        user = request.user

        # 1. GET: Joriy ma'lumotlarni ko'rish
        if request.method == 'GET':
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            })

        # 2. PATCH: Faqat username, email, password o'zgartirish
        account_data = request.data.get('account')
        if not account_data:
            return Response({"error": "Ma'lumotlar 'account' kaliti ichida yuborilishi kerak"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Serializer orqali validatsiya (email/username bandligini tekshiradi)
        serializer = UserSerializer(user, data=account_data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Servis orqali bazaga saqlash
        updated_user = ProfileService.update_account_data(user, serializer.validated_data)

        return Response({
            "message": "Ma'lumotlar muvaffaqiyatli yangilandi",
            "account": {
                "username": updated_user.username,
                "email": updated_user.email
            }
        }, status=status.HTTP_200_OK)



# class UserBalanceAPI(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = []
#
#     def get(self, request):
#         try:
#             user = self.request.user
#             print(user.username)
#             if user.is_staff or user.is_superuser:
#                 balance = Profile.objects.filter(user=user).first()
#                 if not balance:
#                     return Response(
#                         {"status": status.HTTP_404_NOT_FOUND,
#                          "data": "Foydalanuvchi profili topilmadi!"},
#                         status=status.HTTP_404_NOT_FOUND)
#
#                 serializer = UserProfileSerializer(balance)
#                 return Response({"data": serializer.data,
#                                  "status": status.HTTP_200_OK},
#                                 status=status.HTTP_200_OK)
#
#             else:
#                 return Response({"status": status.HTTP_401_UNAUTHORIZED,
#                                  "data": "Profilni ko'rish uchun sizda ruxsat yo'q !"},
#                                 status=status.HTTP_401_UNAUTHORIZED)
#
#
#         except Exception as e:
#             print(e)
#             return Response(
#                 {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
#
