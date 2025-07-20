from rest_framework import generics

from materials.models import Lesson


class GetQuerysetMixin:
    """
    Миксин для создания следующих прав:
    админы и модеры имеют доступ ко всем объектам
    остальные имеют доступ только ко своим объектам
    """

    def is_list(self):
        if getattr(self, 'action', None) == 'list':
            return True
        return isinstance(self, generics.ListAPIView)

    def get_queryset(self):

        qrst = super().get_queryset()
        user = self.request.user

        if self.is_list():
            if user.is_staff or user.groups.filter(name="moders").exists():
                return qrst
            return qrst.filter(owner=user)
        else:
            return qrst
