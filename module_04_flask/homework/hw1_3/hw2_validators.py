"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field, ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: Field):
        phone_len = len(str(field.data))
        if phone_len < min or phone_len > max:
            raise ValidationError(message)

    return  _number_length


class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        phone_len = len(str(field.data))
        if phone_len < self.min or phone_len > self.max:
            raise ValidationError(self.message)