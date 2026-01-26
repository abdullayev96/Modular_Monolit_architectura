from django.db import transaction
from .models import User
from profile.services import create_user_profile # Modullararo aloqa


def register_user_logic(email, username, password):
    """
    Modular Monolith mantiqi: Userni yaratish va unga boshqa modulda profil ochish.
    """
    with transaction.atomic():
        # 1. Userni yaratish (is_staff va role modelda ko'rsatilgan defaultni oladi)
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        # 2. Profilni yaratish (ID orqali loose coupling)
        create_user_profile(user_id=user.id)

        return user