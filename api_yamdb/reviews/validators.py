import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    year = datetime.date.today().year
    if (year < value):
        raise ValidationError(
            'Год не может быть меньше текущего года!'
        )
    return value
