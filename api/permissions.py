from rest_framework import permissions
from api.models import User


def is_safe_request(request):
    return request.method in permissions.SAFE_METHODS


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if is_safe_request(request):
            return True
        staff_user = (request.user.role in User.PRIVILEGED_USERS
                      or request.user.is_superuser)
        return obj.author == request.user or staff_user


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (is_safe_request(request)
                or (user.is_authenticated
                    and (user.role == user.RoleChoices.ADMIN or user.is_staff)))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and (user.role == user.RoleChoices.ADMIN or user.is_staff))
