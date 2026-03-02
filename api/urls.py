from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, StatViewSet, TruckViewSet

router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'stats', StatViewSet, basename='stat')

urlpatterns = [
    path('', include(router.urls)),
]
