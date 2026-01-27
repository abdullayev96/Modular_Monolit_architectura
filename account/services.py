from django.db import transaction
from .models import User
from profiles.service import create_user_profile

def register_user_logic(email, username, password):
    with transaction.atomic():
        # 1. Userni yaratish
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        # 2. Profil moduliga xabar berish (Loose Coupling)
        create_user_profile(user_id=user.id)

        return user