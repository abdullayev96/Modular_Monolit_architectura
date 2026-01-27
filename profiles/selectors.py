from account.models import User
from .models import Profile


def get_profile_details(user_id: int):
    profile = Profile.objects.get(user_id=user_id)
    user = User.objects.get(id=user_id)

    return {
        "username": user.username,
        "email": user.email,
        "balance": profile.balance,
        "purchased_books_count": len(profile.purchased_book_ids)
    }