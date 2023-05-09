from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.apps.meteo.managers import CityManager


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=(MaxValueValidator(90), MinValueValidator(-90.0)),
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=(MaxValueValidator(180.0), MinValueValidator(-180.0)),
    )

    objects = CityManager()

    def __str__(self):
        return f"{self.name} ({self.longitude}, {self.latitude})"

    class Meta:
        verbose_name_plural = "Cities"
        db_table = "cities"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "longitude", "latitude"], name="unique_city"
            ),
            models.UniqueConstraint(
                fields=["name"],
                condition=(
                    models.Q(longitude__isnull=True) | models.Q(latitude__isnull=True)
                ),
                name="unique_city_without_coordinates",
            ),
        ]
