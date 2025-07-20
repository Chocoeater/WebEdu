from materials.models import Lesson


class GetQuerysetMixin:
    """
    Миксин для создания следующих прав:
    админы и модеры имеют доступ ко всем объектам
    остальные имеют доступ только ко своим объектам
    """

    def get_queryset(self):
        qrst = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.groups.filter(name="moders").exists():
            return qrst
        return qrst.filter(owner=user)
