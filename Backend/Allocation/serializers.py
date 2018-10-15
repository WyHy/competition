from rest_framework import serializers

from .models import Allocation


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = ('id', 'user', 'tiff', 'create_time', 'update_time',)
