from rest_framework.permissions import SAFE_METHODS, IsAdminUser
from rest_framework import permissions


class IsAdminUserOrReadOnly(IsAdminUser):
    """
    Проверка прав доступа для пользователей:
    - Администраторы могут выполнять любые методы.
    - Для всех остальных пользователей доступны только
    безопасные методы (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        """
        Проверяет, имеет ли пользователь права на выполнение запроса.
        """
        is_admin = super(
            IsAdminUserOrReadOnly,
            self).has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class IsAdmin(permissions.BasePermission):
    """IsAdmin permission.
    Разрешает доступ к ресурсу, если пользователь аутентифицирован и является
    администратором или суперпользователем.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )
