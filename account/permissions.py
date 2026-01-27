from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Adminlar uchun to'liq (CRUD), foydalanuvchilar uchun faqat o'qish (ReadOnly).
    Bu Author, Category va Book modellari uchun ideal.
    """
    def has_permission(self, request, view):
        # 1. O'qish so'rovlari (GET, HEAD, OPTIONS) uchun hamma (hatto anonimlar ham) o'ta oladi
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. O'zgartirish (POST, PUT, DELETE) uchun faqat admin va superadmin
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['admin', 'superadmin']
        )

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Profil kabi shaxsiy obyektlar uchun:
    Faqat egasi yoki Admin tahrirlay oladi.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Admin bo'lsa hamma narsaga ruxsat
        if request.user.role in ['admin', 'superadmin']:
            return True

        # Obyekt egasini tekshirish
        owner = getattr(obj, 'user', None) or getattr(obj, 'author', None)
        return owner == request.user