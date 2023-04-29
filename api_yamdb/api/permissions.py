from rest_framework.permissions import SAFE_METHODS, IsAdminUser


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
