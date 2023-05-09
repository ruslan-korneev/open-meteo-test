from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from requests import HTTPError

from src.apps.meteo.services import OpenMeteoBackend


class CityManager(models.Manager):
    @transaction.atomic
    def get_or_create(self, defaults=None, **kwargs):
        city, created = super().get_or_create(**kwargs)
        if not city.longitude or not city.latitude:
            backend = OpenMeteoBackend()
            try:
                data = backend.get_coordinates(city.name)
            except HTTPError:
                raise ObjectDoesNotExist("City not found")

            if not data:
                raise ObjectDoesNotExist("City not found")
            city.longitude = data["longitude"]
            city.latitude = data["latitude"]
            city.save()
        return city, created
