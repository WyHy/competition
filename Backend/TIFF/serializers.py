import os
from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'path', 'progress', 'result_auto', 'result_manual', 'result_status', 'create_time', 'update_time',)


class CompetitionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name')


class CompetitionProgressSerializer(serializers.ModelSerializer):
	name = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'name', 'progress', 'result_auto', 'result_manual')

    def get_name(self, obj):
    	return os.path.basename(obj.name)


class CompetitionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'progress', 'result_auto', 'result_manual', 'result_status')
