from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Кастомизирует пользовательский класс."""

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=CHOICES,
        default='user'
    )
