from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Profile


class ProfileService:
    @staticmethod
    @transaction.atomic
    def update_account_data(user, account_data: dict):
        if not account_data:
            return user

        # Username va Emailni yangilash
        if 'username' in account_data:
            user.username = account_data['username']

        if 'email' in account_data:
            user.email = account_data['email']

        # Parolni xavfsiz yangilash (hash qilish)
        password = account_data.get('password')
        if password:
            user.set_password(password)

        user.save()
        return user

def update_balance(user_id: int, amount: float):
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
