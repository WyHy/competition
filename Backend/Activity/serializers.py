from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from Profile.models import Profile
from .models import Answer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'image', 'profile', 'answer', 'create_time')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'image', 'profile', 'answer', 'create_time')

    def create(self, validated_data):
        image = validated_data.get("image")
        profile = validated_data.get("profile")

        try:
            obj = Answer.objects.get(image=image, profile=profile)
            return super(AnswerSerializer, self).update(obj, validated_data)
        except ObjectDoesNotExist:
            return super(AnswerSerializer, self).create(validated_data)
