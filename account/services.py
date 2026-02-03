from django.db import transaction
from .models import User
from profiles.service import ProfileService

def register_user_logic(email, username, password):
    with transaction.atomic():
        # 1. Userni yaratish
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        ProfileService.update_profile_and_account(user_id=user.id)

    return user