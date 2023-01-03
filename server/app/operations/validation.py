from django.core.exceptions import ValidationError


def validate_operation_cost(value):
    """Проверка, что значение операции должно быть строго больше нуля"""
    if value <= 0:
        raise ValidationError("Значение операции не может быть меньше или равна нулю")
