from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import validate_year


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        """
        Сортирует категории и добавляет русские названия в админке.
        """
        ordering = ('id', )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        """
        Сортирует жанры и добавляет русские названия в админке.
        """
        ordering = ('id', )
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    category = models.ForeignKey(Category, related_name='titles',
                                 on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    description = models.TextField(blank=True, default='to describe')

    class Meta:
        """
        Сортирует произведения и добавляет русские названия в админке.
        """
        ordering = ('id', )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} {self.genres}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'id {self.pk} жанр {self.genre}  title  {self.title}'


class Review(models.Model):
    text = models.TextField(
        verbose_name="Текст отзыва",
        help_text='Напишите свой отзыв здесь'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="author_review",
        verbose_name="Автор"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения"
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10, 'Максимальная оценка - 10'),
            MinValueValidator(1, 'Минимальная оценка - 1')
        ],
        verbose_name="Ваша оценка произведению",
        help_text='Поставьте свою оценку произведению'
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата оценки",
        auto_now_add=True
    )

    class Meta:
        """
        Сортирует, валидирует отзывы и добавляет русские названия в админке.
        """
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author'
            )
        ]
        ordering = ('id', )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text='Напишите свой комментарий'
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата комментария",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="author_comment",
        verbose_name="Автор комментария"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв на произведение"
    )

    class Meta:
        """
        Сортирует комментарии и добавляет русские название в админке.
        """
        ordering = ('id', )
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
