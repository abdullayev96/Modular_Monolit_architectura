from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from profiles.service import get_profile_by_user_id


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Admin ro'yxatida balansni ko'rsatish
    list_display = ('id', 'email', 'first_name', 'last_name', 'get_balance', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_balance(self, obj):
        """
        Profil servisidan foydalanib balansni olib kelish.
        """
        profile = get_profile_by_user_id(user_id=obj.id)
        if profile:
            return f"{profile.balance} so'm"
        return "0.00 so'm"

    # Admin panelda ustun nomi
    get_balance.short_description = 'Foydalanuvchi Balansi'

    # Inline ishlatib bo'lmaydi, shuning uchun uni o'chirib tashlaymiz