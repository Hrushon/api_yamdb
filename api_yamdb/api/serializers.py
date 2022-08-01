from rest_framework import serializers
from reviews.models import Categories, Titles, Genres, GenresTitle
import datetime

from django.db.models import Avg


class GenreValidateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        try:
            obj = Genres.objects.get(slug=data)
        except Exception:
            raise serializers.ValidationError(f'Жанр {data} отсутствует')
        return obj

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CatValidateSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        try:
            obj = Categories.objects.get(slug=data)
        except Exception:
            raise serializers.ValidationError(f'Категория {data} отсутствует')
        return obj

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class CategoryGetMethod(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class GenresGetMethod(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesGettingSerializer(serializers.ModelSerializer):
    """Сериалайзер на GET /titles/ и /titles/id/"""
    genres = GenresGetMethod(many=True)
    category = CategoryGetMethod()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genres', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(rating=Avg('rating'))
        print((rating))
        if (rating.get('rating')) is not None:
            return round(rating.get('rating'), 0)
        return (rating.get('rating'))


class TitlesSerializer(serializers.ModelSerializer):
    """Сериалайзер на POST /titles/"""
    genres = GenreValidateSerializer(many=True)
    category = CatValidateSerializer()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genres', 'category')

    def validate_year(self, value):
        year = datetime.date.today().year
        if (year < value):
            raise serializers.ValidationError('Год создания произведения'
                                              'не м.б. больше текущего!')
        return value

    def create(self, validated_data):
        genres_to_write = validated_data.pop('genres')
        title = Titles.objects.create(**validated_data)
        print(title)
        for genre in genres_to_write:
            GenresTitle.objects.create(title=title, genre=genre)
        return (title)
from django.forms import ValidationError
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Titles, Comments, Review


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
        field = '__all__'


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
        field = '__all__'
