from rest_framework import serializers

from .models import Cell, ScreenShot


class CellSerializer(serializers.ModelSerializer):
    cell_type = serializers.SerializerMethodField()
    x = serializers.SerializerMethodField()
    y = serializers.SerializerMethodField()
    w = serializers.SerializerMethodField()
    h = serializers.SerializerMethodField()

    class Meta:
        model = Cell
        fields = ('id', 'image', 'x', 'y', 'w', 'h', 'cell_type', 'accuracy', 'source_type', 'create_time')

    def get_cell_type(self, obj):
        label = obj.cell_type
        if label in ["MC", "SC", "RC", "GEC"]:
            return "NILM"

        if "_" in label:
            return label.split("_")[0]
        return label

    def get_x(self, obj):
        return obj.x - obj.w / 2

    def get_y(self, obj):
        return obj.y - obj.h / 2

    def get_w(self, obj):
        return 2 * obj.w

    def get_h(self, obj):
        return 2 * obj.h


class ScreenShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreenShot
        fields = ('id', 'image', 'x', 'y', 'w', 'h', 'source_type')
