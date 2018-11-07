import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Type
from .serializers import TypeSerializer


class TypeFilter(filters.FilterSet):
    class Meta:
        model = Type
        fields = ('id',)


class ViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = TypeFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('id',)
