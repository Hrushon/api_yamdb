from rest_framework import permissions


class SelfEditUserOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ к users/me только самим user-ам."""

    def has_object_permission(self, request, view, obj):
        return (obj.id == request.user)


class IsAuthorModeratorAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Обеспечивает доступ автору, модератору и админу.
    Все остальные - безопасные методы.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ админу. Все остальные - безопасные методы."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'admin' or request.user.is_superuser
        )


class IsAdminOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ только aдмину."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin' or request.user.is_superuser
        )
