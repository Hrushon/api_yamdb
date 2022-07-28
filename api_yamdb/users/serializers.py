from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {'email': {'required': True}}


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, validators=[UnicodeUsernameValidator, ]
    )
    confirmation_code = serializers.UUIDField()
