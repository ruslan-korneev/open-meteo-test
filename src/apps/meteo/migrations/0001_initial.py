# Generated by Django 4.2.1 on 2023-05-09 16:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(90),
                            django.core.validators.MinValueValidator(-90.0),
                        ],
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True,
                        decimal_places=6,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(180.0),
                            django.core.validators.MinValueValidator(-180.0),
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cities",
                "db_table": "cities",
            },
        ),
        migrations.CreateModel(
            name="WeatherData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "temperature_2m_max",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "temperature_2m_min",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "precipitation_sum",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "windspeed_10m_max",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
            ],
            options={
                "verbose_name_plural": "Weather Data",
                "db_table": "weather_data",
            },
        ),
        migrations.CreateModel(
            name="Weather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="weather",
                        to="meteo.city",
                    ),
                ),
                (
                    "forecast",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="forecast_weather",
                        to="meteo.weatherdata",
                    ),
                ),
                (
                    "measured",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="measured_weather",
                        to="meteo.weatherdata",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Weather",
                "db_table": "weather",
                "ordering": ["-date"],
            },
        ),
        migrations.AddConstraint(
            model_name="city",
            constraint=models.UniqueConstraint(
                fields=("name", "longitude", "latitude"), name="unique_city"
            ),
        ),
        migrations.AddConstraint(
            model_name="city",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("longitude__isnull", True),
                    ("latitude__isnull", True),
                    _connector="OR",
                ),
                fields=("name",),
                name="unique_city_without_coordinates",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="weather",
            unique_together={("city", "date")},
        ),
    ]
