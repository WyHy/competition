import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Profile
from .serializers import ProfileSerializer, UserCreateSerializer


class ProfileFilter(filters.FilterSet):
    class Meta:
        model = Profile
        fields = ('id', 'type', 'user__username')


class ViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ProfileFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('id',)


class AddUserSet(ViewSet):
    serializer_class = UserCreateSerializer
