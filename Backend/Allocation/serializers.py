from rest_framework import serializers

from TIFF.models import Image
from .models import Allocation


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = ('id', 'profile', 'tiff', 'create_time', 'update_time',)


class CompetitionDoctorResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'case_no', 'result_manual')


class AllocationViewSerializer(serializers.ModelSerializer):
    tiff = CompetitionDoctorResultSerializer(many=False, read_only=True)

    class Meta:
        model = Allocation
        fields = ('id', 'profile', 'tiff', )
