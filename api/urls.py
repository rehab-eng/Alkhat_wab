from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProjectViewSet,
    SiteSettingViewSet,
    StatViewSet,
    StatisticViewSet,
    TruckViewSet,
    VehicleViewSet,
)

router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'stats', StatViewSet, basename='stat')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'statistics', StatisticViewSet, basename='statistic')
router.register(r'site-settings', SiteSettingViewSet, basename='site-setting')

urlpatterns = [
    path('', include(router.urls)),
]
