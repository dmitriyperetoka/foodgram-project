from rest_framework import exceptions


class NotEqualValidator:
    def __init__(self, field_1, field_2, message=None):
        self.field_1 = field_1
        self.field_2 = field_2
        self.message = message or (
            f'Значения полей {self.field_1} '
            f'и {self.field_2} не должны быть одинаковыми.')

    def __call__(self, value):
        if value[self.field_1] == value[self.field_2]:
            raise exceptions.ValidationError(self.message)
