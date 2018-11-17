import rest_framework_filters as filters
from django.db.models import F, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response

from Activity.models import Answer
from Activity.serializers import AnswerSerializer
from Backend import settings
from Middleware.authentication import CsrfExemptSessionAuthentication
from Profile.models import Profile
from TIFF.models import Image

import redis


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

    authentication_classes = (CsrfExemptSessionAuthentication,)


class StatisticViewSet(ViewSet):
    """
    观众答题统计接口
    """

    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        return Response(data={"status": "OK"}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        images = Image.objects.exclude(result_status__exact='-')
        if images.count() != 40:
            return Response(data={'err': 'The standard diagnose result is not complete, Please check and try again'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # the answer is right if gamer's answer is contained in standard diagnose result
        activies = Answer.objects.filter(image__result_status__contains=F('answer__name')).values('profile').annotate(
            count=Count('profile')).order_by("-count")

        data = []
        for item in activies:
            profile = Profile.objects.get(id=item['profile'])
            data.append({'name': profile.nickname, "count": item['count'], "tel": profile.user.username})

        return Response(data=data, status=status.HTTP_200_OK)


class GameStatusControlView(APIView):
    def get(self, request, format=None):
        game_status = request.GET.get('status')

        if game_status == "0":
            settings.redis_connection.set('status', '0')
            return Response(data={"msg": "比赛中止"}, status=status.HTTP_200_OK)
        elif game_status == "1":
            settings.redis_connection.set('status', '1')
            return Response(data={"msg": "比赛开始"}, status=status.HTTP_200_OK)
        elif not game_status:
            return Response(data={"status": settings.redis_connection.get('status')}, status=status.HTTP_200_OK)

        return Response(data={"msg": "未识别的比赛状态控制命令"}, status=status.HTTP_406_NOT_ACCEPTABLE)
