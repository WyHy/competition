import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import UserType
from .serializers import UserTypeSerializer


class UserTypeFilter(filters.FilterSet):
    class Meta:
        model = UserType
        fields = ('id',)


class ViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = UserTypeFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('-id',)
