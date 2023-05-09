from django.db import models


class WeatherData(models.Model):
    temperature_2m_max = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_2m_min = models.DecimalField(max_digits=5, decimal_places=2)
    precipitation_sum = models.DecimalField(max_digits=5, decimal_places=2)
    windspeed_10m_max = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Weather Data"
        db_table = "weather_data"

    @classmethod
    def fields(cls):
        return [
            field.name
            for field in cls._meta.get_fields()
            if not field.is_relation and not field.auto_created
        ]


class Weather(models.Model):
    city = models.ForeignKey(
        "meteo.City", on_delete=models.CASCADE, related_name="weather"
    )
    date = models.DateField()
    measured = models.OneToOneField(
        "meteo.WeatherData",
        on_delete=models.CASCADE,
        related_name="measured_weather",
        null=True,
        blank=True,
    )
    forecast = models.OneToOneField(
        "meteo.WeatherData",
        on_delete=models.CASCADE,
        related_name="forecast_weather",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.city.name} | {self.date}"

    class Meta:
        verbose_name_plural = "Weather"
        ordering = ["-date"]
        db_table = "weather"
        unique_together = ("city", "date")
