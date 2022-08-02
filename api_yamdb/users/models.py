import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Кастомизирует пользовательский класс."""

    email = models.EmailField(
        'Адрес электронной почты',
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=CHOICES,
        default='user',
    )
    confirmation_code = models.UUIDField(
        'Код для получения/обновления токена',
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    class Meta:
        """
        Сортирует пользователей и добавляет русские название в админке.
        """
        ordering = ('-id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
