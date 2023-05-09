import json
import csv
import os

from django.conf import settings

from src.apps.meteo.api.serializers import WeatherSerializer
from src.apps.meteo.models.weather import Weather, WeatherData


def create_folder_if_not_exists(func):
    def wrapper(*args, **kwargs):
        if not os.path.exists(settings.WEATHER_DATA_PATH):
            os.makedirs(settings.WEATHER_DATA_PATH)
        return func(*args, **kwargs)

    return wrapper


@create_folder_if_not_exists
def save_in_json(filename: str, data: list["Weather"]) -> str:
    """
    Save weather data in json format.
    """
    serializer = WeatherSerializer(instance=data, many=True)
    path_to_file = os.path.join(settings.WEATHER_DATA_PATH, f"{filename}.json")
    with open(path_to_file, "w") as file:
        json.dump(serializer.data, file, indent=4)

    return path_to_file


@create_folder_if_not_exists
def save_in_csv(filename: str, data: list["Weather"]) -> str:
    """
    Save weather data in csv format.
    """
    path_to_file = os.path.join(settings.WEATHER_DATA_PATH, f"{filename}.csv")
    with open(path_to_file, "w") as file:
        writer = csv.writer(file)
        writer.writerow(
            ("city", "date", "is_measured", *(fields := WeatherData.fields()))
        )
        for weather in data:
            if weather.measured:
                writer.writerow(
                    (
                        weather.city.name,
                        weather.date,
                        True,
                        *[getattr(weather.measured, field) for field in fields],
                    )
                )
            if weather.forecast:
                writer.writerow(
                    (
                        weather.city.name,
                        weather.date,
                        False,
                        *[getattr(weather.forecast, field) for field in fields],
                    )
                )

    return path_to_file
