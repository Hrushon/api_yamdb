from django.db import models
import sqlite3


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Categories, related_name='titles', on_delete=models.PROTECT)
    genres = models.ManyToManyField(Genres, through='GenresTitle')
    description = models.TextField(null=True)

    def get_genres(self):
        return list(self.genres.all())

    def __str__(self):
        return f'{self.name} {self.genres}'


class GenresTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'id {self.pk} жанр {self.genre}  title  {self.title}'
