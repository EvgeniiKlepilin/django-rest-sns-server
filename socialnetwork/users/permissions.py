from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return request.user.is_staff
        else:
            return obj == request.user or request.user.is_staff

class AllowAnyCreate(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True