import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

# Create your views here.
from Activity.models import Answer
from Activity.serializers import AnswerSerializer


class AnswerFilter(filters.FilterSet):
    class Meta:
        model = Answer
        fields = ('id', 'profile')


class ViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = AnswerFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('id',)
