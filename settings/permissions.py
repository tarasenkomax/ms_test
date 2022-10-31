from rest_framework import permissions


class IsCuratorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        """ Доступ для чтения для куратора """
        if request.user.is_authenticated:
            if request.method == 'GET' and request.user.profile.is_curator:
                return True
        else:
            return False


class IsCurator(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        """ Доступ куратору """
        if request.user.is_authenticated:
            if request.user.profile.is_curator:
                return True
        else:
            return False
