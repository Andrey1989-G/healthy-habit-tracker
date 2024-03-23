from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """система аутентификации и авторизации пользователей"""

    def has_permission(self, request, view):
        return request.user == view.get_object().owner
