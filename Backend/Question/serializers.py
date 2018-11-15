from rest_framework import serializers

from PathologyType.models import Type
from TIFF.models import Image
from .models import Question


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'case_no')


class QuestionSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=False, read_only=True)
    choices = TypeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'image', 'choices', 'remark')
