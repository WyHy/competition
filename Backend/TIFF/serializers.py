from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
        'id', 'name', 'case_no', 'path', 'progress', 'result_auto', 'result_manual', 'result_status', 'create_time',
        'update_time',)


class CompetitionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name''case_no',)


class CompetitionProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'case_no', 'progress', 'result_auto', 'result_manual')


class CompetitionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'case_no', 'progress', 'result_auto', 'result_manual', 'result_status')
