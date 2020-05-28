from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class OnlyAdminCanDelete(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_superuser
        return False

class AllowAnyCreate(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True