import uuid

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Project, SiteSetting, Stat, Statistic, Truck, Vehicle
from .serializers import (
    ProjectSerializer,
    SiteSettingSerializer,
    StatSerializer,
    StatisticSerializer,
    TruckSerializer,
    VehicleSerializer,
)


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all().order_by('-id')
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-date', '-id')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class StatViewSet(viewsets.ModelViewSet):
    queryset = Stat.objects.all().order_by('order', 'id')
    serializer_class = StatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('-updated_at', '-id')
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class StatisticViewSet(viewsets.ModelViewSet):
    queryset = Statistic.objects.all().order_by('order', 'id')
    serializer_class = StatisticSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]


class SiteSettingViewSet(viewsets.ModelViewSet):
    queryset = SiteSetting.objects.all().order_by('-updated_at', '-id')
    serializer_class = SiteSettingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        setting = SiteSetting.objects.first()
        if setting is None:
            setting = SiteSetting.objects.create()
        setting.refresh_token = uuid.uuid4()
        setting.save(update_fields=['refresh_token', 'updated_at'])
        serializer = self.get_serializer(setting)
        return Response(serializer.data)
