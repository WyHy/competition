import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Allocation
from .serializers import AllocationSerializer, AllocationViewSerializer


class AllocationFilter(filters.FilterSet):
    class Meta:
        model = Allocation
        fields = ('id', 'profile')


class ViewSet(viewsets.ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = AllocationFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('id',)

    def get_serializer_class(self):
        # if self.request.method == 'GET':
        #     return AllocationViewSerializer

        if self.request.method == 'POST':
            return AllocationSerializer

        return AllocationViewSerializer
