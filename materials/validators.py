import re

from rest_framework import serializers


class LinkValidator:
    """
    Проверяет, на youtube ли ссылка.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = value.get(self.field)

        if not tmp_val:
            return

        pattern = re.compile(
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        )
        if not pattern.match(tmp_val):
            raise serializers.ValidationError('Данная ссылка не поддерживается')
