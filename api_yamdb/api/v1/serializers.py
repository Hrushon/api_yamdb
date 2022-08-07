from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesGettingSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ['__all__']


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def to_representation(self, value):
        return TitlesGettingSerializer(value).data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if (value == 'me'):
            raise serializers.ValidationError(
                'Запрещено использовать me в качестве username'
            )
        return value


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if (value == 'me'):
            raise serializers.ValidationError(
                'Запрещено использовать me в качестве username'
            )
        return value


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator, ]
    )
    confirmation_code = serializers.CharField()
