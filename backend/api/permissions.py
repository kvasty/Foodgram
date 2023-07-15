from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Создание и изменение доступно только автору"""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsAdminOrReadOnly(BasePermission):
    """Создание и изменение доступно только админу"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_staff)
