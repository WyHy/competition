import rest_framework_filters as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from Backend import settings
from .models import Image
from .serializers import ImageSerializer, CompetitionQuestionSerializer, CompetitionProgressSerializer, \
    CompetitionResultSerializer


class ImageFilter(filters.FilterSet):
    class Meta:
        model = Image
        fields = ('id', 'name')


class ViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.filter(is_valid='YES')
    serializer_class = ImageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ImageFilter
    lookup_field = 'id'
    ordering_fields = ('id', 'create_time',)
    ordering = ('id',)

    def update(self, request, *args, **kwargs):
        if settings.redis_connection.get('status') == "0":
            return Response(data={"msg": "比赛尚未开始，请等待！"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(ViewSet, self).update(request, *args, **kwargs)


class QuestionViewSet(ViewSet):
    serializer_class = CompetitionQuestionSerializer


class ProgressViewSet(ViewSet):
    serializer_class = CompetitionProgressSerializer


class ResultViewSet(ViewSet):
    serializer_class = CompetitionResultSerializer
