from rest_framework import serializers

from .models import Type


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'name', 'description', 'create_time', 'update_time',)
