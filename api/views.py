from rest_framework import permissions, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import Project, Stat, Truck
from .serializers import ProjectSerializer, StatSerializer, TruckSerializer


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
