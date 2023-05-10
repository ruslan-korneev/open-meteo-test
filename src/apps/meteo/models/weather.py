from django.db import models


class WeatherData(models.Model):
    temperature_2m_max = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_2m_min = models.DecimalField(max_digits=5, decimal_places=2)
    precipitation_sum = models.DecimalField(max_digits=5, decimal_places=2)
    windspeed_10m_max = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Weather Data"
        db_table = "weather_data"
        constraints = [
            models.CheckConstraint(
                check=models.Q(temperature_2m_max__gte=models.F("temperature_2m_min")),
                name="temperature_2m_max_gte_temperature_2m_min",
            ),
            # TODO: fix this constraint's issue: refers to the nonexistent field
            # models.CheckConstraint(
            #     check=models.Q(
            #         measured_weather__isnull=False, forecast_weather__isnull=False
            #     ),
            #     name="weather_data_should_be_forecast_or_measured",
            # ),
        ]

    def clean(self) -> None:
        if self.temperature_2m_max >= self.temperature_2m_min:
            raise ValueError(
                "temperature_2m_max must be greater than or equal to temperature_2m_min"
            )
        if not (self.is_measured or self.is_forecast):
            raise ValueError("Weather data must be measured or forecast")

    def __str__(self) -> str:
        return (
            f"{self.weather} |"
            f"({self.temperature_2m_max}, {self.temperature_2m_min}, "
            f"{self.precipitation_sum}, {self.windspeed_10m_max})"
        )

    @property
    def is_measured(self) -> bool:
        return hasattr(self, "measured_weather")

    @property
    def is_forecast(self) -> bool:
        return hasattr(self, "forecast_weather")

    @property
    def weather(self) -> "Weather":
        weather = getattr(self, "measured_weather", None) or getattr(
            self, "forecast_weather", None
        )
        if not weather:
            raise AttributeError("Weather data must be measured or forecast")

        return weather

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
        on_delete=models.SET_NULL,
        related_name="measured_weather",
        null=True,
        blank=True,
    )
    forecast = models.OneToOneField(
        "meteo.WeatherData",
        on_delete=models.SET_NULL,
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
