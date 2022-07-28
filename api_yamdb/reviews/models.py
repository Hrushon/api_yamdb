from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
