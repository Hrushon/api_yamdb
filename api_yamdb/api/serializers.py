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
