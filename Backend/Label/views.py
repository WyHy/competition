import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Cell
from .serializers import CellSerializer


# Create your views here.
class CellFilter(filters.FilterSet):
    class Meta:
        model = Cell
        fields = ('id',)


class ViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = CellFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('-id',)
