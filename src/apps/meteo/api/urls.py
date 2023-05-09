from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.apps.meteo.api.views import WeatherViewSet


router = DefaultRouter()
router.register("weather", WeatherViewSet, basename="weather")

urlpatterns = [
    path("", include(router.urls)),
]
