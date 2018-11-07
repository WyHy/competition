from rest_framework import serializers

from PathologyType.serializers import TypeSerializer
from .models import Cell, ScreenShot


class CellSerializer(serializers.ModelSerializer):
    # cell_type = TypeSerializer(many=False, read_only=True)

    class Meta:
        model = Cell
        fields = ('id', 'image', 'x', 'y', 'w', 'h', 'cell_type', 'create_time')


class ScreenShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenShot
        fields = ('id', 'image', 'x', 'y', 'w', 'h', 'source_type')



