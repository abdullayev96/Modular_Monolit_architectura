from rest_framework.permissions import BasePermission


class IsAuthenticatedAndActive(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)



class IsSuperAdmin(BasePermission):
    """Tizim egasi uchun (Siz)"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'superadmin')



class IsCompanyAdmin(BasePermission):
    """Kompaniya rahbari uchun"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsCompanyEmployee(BasePermission):
    """Oddiy xodim uchun"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'user')


class IsTenantUser(BasePermission):
    """
    Vazifasi: Foydalanuvchi va obyekt (mashina, yuk, haydovchi)
    bitta kompaniyaga tegishli ekanligini tekshirish.
    """

    def has_object_permission(self, request, view, obj):
        # 1. Foydalanuvchi login qilganini tekshirish
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. SuperAdmin uchun hamma narsaga ruxsat berish (ixtiyoriy)
        if request.user.role == 'superadmin':
            return True

        # 3. Obyektda 'tenant' fieldi borligini tekshirish
        obj_tenant = getattr(obj, 'tenant', None)

        # 4. Moslikni tekshirish
        return obj_tenant == request.user.tenant



class CanAccessUser(BasePermission):
    """
    Vazifasi: Foydalanuvchi ma'lumotlariga kirishni iyerarxiya bo'yicha cheklash.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # 1. Login qilganini tekshirish (Eng birinchi shart)
        if not user or not user.is_authenticated:
            return False

        # 2. SuperAdmin - hamma narsaga ruxsat
        if user.role == 'superadmin':
            return True

        # 3. User va Obyekt tenantlari mosligini tekshirish
        # (Bu yerda 'obj' bu User modelining instansi deb qaraladi)
        if hasattr(obj, 'tenant') and obj.tenant == user.tenant:
            # Kompaniya admini o'z tenantidagi hammani ko'ra oladi
            if user.role == 'admin':
                return True

            # Oddiy xodim faqat o'zi bo'lsa ko'ra oladi
            if user.role == 'user' and obj == user:
                return True

        return False