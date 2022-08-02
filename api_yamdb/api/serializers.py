import datetime

from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class Categ2TitleSerializer(serializers.Field):
    def to_internal_value(self, data):
        try:
            obj = Category.objects.get(slug=data)
        except Exception:
            raise serializers.ValidationError(f'Категория {data} отсутствует')
        return obj

    def to_representation(self, value):
        category = {
            "name": value.name,
            "slug": value.slug
        }
        return category


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesGettingSerializer(serializers.ModelSerializer):
    """Сериалайзер на GET /titles/ и /titles/id/"""
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg('score'))
        if (rating.get('rating')) is not None:
            return round(rating.get('rating'), 0)
        return rating.get('rating')


class TitlesSerializer(serializers.ModelSerializer):
    """Сериалайзер на POST /titles/"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = Categ2TitleSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg('score'))
        if (rating.get('rating')) is not None:
            return round(rating.get('rating'), 0)
        return rating.get('rating')

    def validate_year(self, value):
        year = datetime.date.today().year
        if (year < value):
            raise serializers.ValidationError(
                'Год не может быть меньше текущего года!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if 1 > value > 10:
            raise ValidationError(
                "Нужно указать оценку в диапазоне от 1 до 10"
            )
        return value

    def validate(self, data):
        title = get_object_or_404(
            Title, id=self.context['view'].kwargs.get('title_id')
        )
        user = self.context.get('request').user
        if Review.objects.filter(title=title, author=user).exists():
            if self.context['request'].method in ['POST']:
                raise serializers.ValidationError(
                    'Нельзя оставить более одного отзыва'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
