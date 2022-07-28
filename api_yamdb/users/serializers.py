from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        extra_kwargs = {'email': {'required': True}}


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('confirmation_code',)
