from django.db import IntegrityError
from .models import Profile

def create_user_profile(user_id: int):

    try:
        profile = Profile.objects.create(user_id=user_id)
        return profile
    except IntegrityError:
        # Agar ushbu user_id uchun profil allaqachon mavjud bo'lsa
        return None

def update_balance(user_id: int, amount: float):
    """Foydalanuvchi balansini o'zgartirish servisi."""
    profile = Profile.objects.get(user_id=user_id)
    profile.balance += amount
    profile.save()
    return profile


def get_profile_by_user_id(user_id):
    """Admin yoki View-lar uchun profilni olish servisi."""
    try:
        return Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return None
