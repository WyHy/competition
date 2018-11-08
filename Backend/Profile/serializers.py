from django.contrib.auth.models import User
from rest_framework import serializers

from Backend import settings
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'nickname', 'user', 'type', 'create_time', 'update_time',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)


class UserCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False,)

    class Meta:
        model = Profile
        fields = ('id', 'nickname', 'type', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        user_data.update({
            'password': settings.CUSTOM['default_password'],
            'is_active': False
        })
        user = User.objects.create(**user_data)
        user.save()

        validated_data.update({
            "user": user,
        })

        profile = Profile.objects.create(**validated_data)
        profile.save()

        return profile
