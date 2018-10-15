from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'path', 'progress', 'result_auto', 'result_manual', 'result_status', 'create_time', 'update_time',)
