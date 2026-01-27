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
from .serializers import ProfileSerializer, UserSerializer
from account.permissions import *


class ProfileAPI(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'superadmin']:
            return Profile.objects.all()
        return Profile.objects.filter(user_id=user.id)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        profile = get_object_or_404(Profile, user_id=user.id)

        if request.method == 'GET':
            return Response({
                "account": UserSerializer(user).data,
                "profile": ProfileSerializer(profile).data
            })

        account_data = request.data.get('account')
        if account_data:
            user_serializer = UserSerializer(user, data=account_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        profile_data = request.data.get('profile')
        if profile_data:
            # Xavfsizlik uchun balansni tahrirlashni taqiqlaymiz
            profile_data.pop('balance', None)
            profile_serializer = ProfileSerializer(profile, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        return Response({"message": "Ma'lumotlar muvaffaqiyatli yangilandi"})

    def get_permissions(self):
        # Action-larga qarab permissionlarni taqsimlash
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['list', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]



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
