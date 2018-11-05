from rest_framework import serializers

from TIFF.serializers import CompetitionQuestionSerializer
from .models import Allocation


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = ('id', 'profile', 'tiff', 'create_time', 'update_time',)


class AllocationViewSerializer(serializers.ModelSerializer):
    tiff = CompetitionQuestionSerializer(many=False, read_only=True)

    class Meta:
        model = Allocation
        fields = ('profile', 'tiff', )
