from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.base import BaseCommand
from django.db import models, transaction
from requests import HTTPError
from rest_framework.exceptions import ValidationError as DRFValidationError

from src.apps.meteo.api.serializers import GetWeatherSerializer
from src.apps.meteo.exceptions import OpenMeteoValidationError
from src.apps.meteo.models.cities import City
from src.apps.meteo.models.weather import Weather
from src.apps.meteo.services import OpenMeteoBackend, save_in_json, save_in_csv


class OutputFormats(models.TextChoices):
    json = "json", "json"
    csv = "csv", "csv"


class Command(BaseCommand):
    help = "Get weather data from OpenMeteo API."
    SAVE_IN_FILE_METHODS = {
        OutputFormats.json: save_in_json,
        OutputFormats.csv: save_in_csv,
    }

    def add_arguments(self, parser):
        parser.add_argument("city_name", type=str, help="City name.")
        parser.add_argument(
            "start_date", type=str, help="Start date in format YYYY-MM-DD."
        )
        parser.add_argument("end_date", type=str, help="End date in format YYYY-MM-DD.")
        parser.add_argument(
            "output",
            type=str,
            choices=OutputFormats,
            nargs="?",
            help="Output format",
            default=OutputFormats.csv,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # Validating input
        output = options.pop("output")
        serializer = GetWeatherSerializer(data=options)
        try:
            serializer.is_valid(raise_exception=True)
        except DRFValidationError as e:
            self.stdout.write(self.style.ERROR(str(e)))
            raise SystemExit(1)

        # Fetching city
        try:
            city, _ = City.objects.get_or_create(
                name=serializer.validated_data["city_name"]
            )
        except ObjectDoesNotExist:
            self.stdout.write(
                self.style.HTTP_NOT_FOUND(
                    f"City {serializer.validated_data['city_name']} "
                    "does not exist in OpenMeteo GEO API. "
                    f"Please check the city name."
                )
            )
            raise SystemExit(1)

        # Fetching weather
        backend = OpenMeteoBackend()
        try:
            result = backend.get_weather_for_city(
                city=city, **serializer.validated_data
            )
        except (OpenMeteoValidationError, HTTPError) as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error while getting weather data from OpenMeteo API: {e}"
                )
            )
            raise SystemExit(1)
        except ValidationError as e:
            self.stdout.write(
                self.style.WARNING(f"Error while saving weather data to database: {e}")
            )
            result = Weather.objects.filter(
                city=city,
                date__range=(
                    serializer.validated_data["start_date"],
                    serializer.validated_data["end_date"],
                ),
            )

        # Checking if there is any data
        if not result:
            self.stdout.write(
                self.style.WARNING(
                    f"No weather data for city {city.name} "
                    f"between {serializer.validated_data['start_date']} "
                    f"and {serializer.validated_data['end_date']}"
                )
            )
            return

        # Saving weather data
        path_to_file = self.save_weather_data(list(result), output)
        self.stdout.write(
            self.style.SUCCESS(
                f"Weather data has been downloaded successfully to {path_to_file} file."
                f" {len(result)} records has been created.\n"
                f" City: {city.name}, start_date: {serializer.validated_data['start_date']},"
                f" end_date: {serializer.validated_data['end_date']}\n"
            )
        )

    def save_weather_data(self, data: list[Weather], output: OutputFormats):
        filename = f"weather_data_{data[0].city.name}_{data[0].date}_{data[-1].date}"
        path_to_file = self.SAVE_IN_FILE_METHODS[output](filename, data)
        return path_to_file
