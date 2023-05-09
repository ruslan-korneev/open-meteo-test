from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from src.apps.base.api.mixins import SerializerPerAction
from src.apps.meteo.api.filters import WeatherFilterSet
from src.apps.meteo.api.serializers import (
    ForecastMeasuredDifferenceSerializer,
    WeatherSerializer,
)
from src.apps.meteo.models.weather import Weather


class WeatherViewSet(SerializerPerAction, ListModelMixin, GenericViewSet):
    queryset = Weather.objects.all()
    filterset_class = WeatherFilterSet
    action_serializer = {
        "default": WeatherSerializer,
        "difference": ForecastMeasuredDifferenceSerializer,
    }

    def get_queryset(self):
        self.queryset = super().get_queryset()
        if self.action == "difference":
            self.queryset = self.queryset.filter(
                measured__isnull=False, forecast__isnull=False
            )
        return self.queryset

    @action(detail=False, methods=["get"])
    def difference(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
