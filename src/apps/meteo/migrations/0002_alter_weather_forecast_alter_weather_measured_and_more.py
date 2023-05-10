# Generated by Django 4.2.1 on 2023-05-10 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("meteo", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weather",
            name="forecast",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="forecast_weather",
                to="meteo.weatherdata",
            ),
        ),
        migrations.AlterField(
            model_name="weather",
            name="measured",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="measured_weather",
                to="meteo.weatherdata",
            ),
        ),
        migrations.AddConstraint(
            model_name="weatherdata",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("temperature_2m_max__gte", models.F("temperature_2m_min"))
                ),
                name="temperature_2m_max_gte_temperature_2m_min",
            ),
        ),
    ]