from rest_framework.permissions import BasePermission


class IsModer(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()
