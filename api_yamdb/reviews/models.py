from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
<<<<<<< HEAD
from users.models import User
=======
<<<<<<< HEAD
from users.models import User
import sqlite3
=======

from users.models import User
>>>>>>> ed2040466236dac99f633e7a595a839b39642b46
>>>>>>> 121a2918f100eb09c135b14d4590b7f21e24522f


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Categories, related_name='titles',
                                 on_delete=models.PROTECT)
    genres = models.ManyToManyField(Genres, through='GenresTitle')
    description = models.TextField(null=True, default='to describe')

    def get_genres(self):
        return list(self.genres.all())

    def __str__(self):
        return f'{self.name} {self.genres}'


class GenresTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

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
        Titles, on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения"
    )
    rating = models.SmallIntegerField(
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
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
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
        related_name="review",
        verbose_name="Отзыв на произведение"
    )

    def __str__(self):
        return self.text
