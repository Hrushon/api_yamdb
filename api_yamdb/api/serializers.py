import datetime

from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import (
    Categories,
    Comments,
    Genres,
    GenresTitle,
    Review,
    Titles,
)


class GenreValidateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CatValidateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print(data)
        try:
            obj = Categories.objects.get(slug=data)
        except Exception:
            raise serializers.ValidationError(f'Категория {data} отсутствует')
        return obj

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class GenresGetMethod(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesGettingSerializer(serializers.ModelSerializer):
    """Сериалайзер на GET /titles/ и /titles/id/"""
    genre = GenresGetMethod(many=True)
    category = CategoriesSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg('rating'))
        if (rating.get('rating')) is not None:
            return round(rating.get('rating'), 0)
        return 0


class TitlesSerializer(serializers.ModelSerializer):
    """Сериалайзер на POST /titles/"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg('rating'))
        if (rating.get('rating')) is not None:
            return round(rating.get('rating'), 0)
        return 0

    def validate_year(self, value):
        year = datetime.date.today().year
        if (year < value):
            raise serializers.ValidationError('Год создания произведения'
                                              'не м.б. больше текущего!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 1 > value > 10:
            raise ValidationError(
                "Нужно указать оценку в диапазоне от 1 до 10"
            )
        return value

    def validate(self, data):
        title = get_object_or_404(
            Titles, id=self.context['view'].kwargs.get('title_id')
        )
        user = self.context.get('request').user
        if Review.objects.filter(title=title, author=user).exists():
            if self.context['request'].method in ['POST']:
                raise serializers.ValidationError(
                    'Нельзя оставить более одного отзыва'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


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
        model = Comments
        fields = '__all__'
