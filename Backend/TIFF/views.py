import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Image
from .serializers import ImageSerializer


class ImageFilter(filters.FilterSet):
    class Meta:
        model = Image
        fields = ('id',)


class ViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ImageFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('-id',)
