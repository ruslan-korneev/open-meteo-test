from datetime import date
from typing import TYPE_CHECKING

import requests
from django.conf import settings
from django.core.exceptions import ValidationError

from src.apps.meteo.exceptions import OpenMeteoValidationError
from src.apps.meteo.models.weather import Weather, WeatherData

if TYPE_CHECKING:
    from src.apps.meteo.models.cities import City


class OpenMeteoBackend:
    __fields_for_fetch: tuple[str]

    def __init__(self):
        self.__fields_for_fetch = tuple(WeatherData.fields())

    @staticmethod
    def send_request(base_url: str, endpoint: str, **params):
        response = requests.get(f"{base_url}{endpoint}", params=params)
        data = response.json()
        if "error" in data:
            raise OpenMeteoValidationError(data["reason"])

        response.raise_for_status()
        return data

    def get_coordinates(self, city_name: str) -> dict | None:
        """
        Get city coordinates from OpenMeteo API.
        """
        data = self.send_request(settings.OPEN_METEO_GEO_API, "search", name=city_name)
        return data["results"][0] if "results" in data else None

    def get_weather_for_city(
        self,
        city: "City",
        start_date: date,
        end_date: date,
        **kwargs,
    ) -> list[Weather]:
        """
        Get weather data from OpenMeteo API.
        """
        params = {
            "latitude": float(city.latitude),
            "longitude": float(city.longitude),
            "start_date": str(start_date),
            "end_date": str(end_date),
            "daily": ",".join(self.__fields_for_fetch),
            "timezone": settings.TIME_ZONE,
        }
        # assert False, params
        forecast_data = self.send_request(settings.OPEN_METEO_API, "forecast", **params)
        measured_data = self.send_request(
            settings.OPEN_METEO_HISTORICAL_API, "archive", **params
        )

        weathers = []
        weather_data = []
        for index in range((end_date - start_date).days + 1):
            # get or create weather for date
            weather, complete = self.get_weather_if_not_complete(
                city, forecast_data["daily"]["time"][index]
            )
            if complete:
                continue

            # create weather data
            weather = self.create_weather_data(
                weather, forecast_data["daily"], measured_data["daily"], index
            )

            # append weather data to lists to bulk create
            if weather.measured is not None:
                weather_data.append(weather.measured)
            if weather.forecast is not None:
                weather_data.append(weather.forecast)
            if weather.pk is None:
                weathers.append(weather)

        WeatherData.objects.bulk_create(weather_data)
        return Weather.objects.bulk_create(weathers)

    @staticmethod
    def get_weather_if_not_complete(city: "City", date_: date) -> tuple[Weather, bool]:
        """
        Get weather data from database or create.
        if it is not complete sends False as second argument.
        """
        weather = Weather(city=city, date=date_)
        try:
            weather.validate_unique()
        except ValidationError:
            weather = Weather.objects.get(city=city, date=weather.date)
            if weather.measured is not None and weather.forecast is not None:
                return weather, True
        return weather, False

    def create_weather_data(
        self,
        weather,
        measured_data: dict,
        forecast_data: dict,
        index: int,
    ) -> Weather:
        """
        Create weather data.
        """
        measured_weather = WeatherData()
        forecast_weather = WeatherData()
        for field in self.__fields_for_fetch:
            setattr(measured_weather, field, measured_data[field][index])
            setattr(forecast_weather, field, forecast_data[field][index])

        weather.measured = (
            measured_weather
            if getattr(measured_weather, self.__fields_for_fetch[0], None)
            else None
        )
        weather.forecast = (
            forecast_weather
            if getattr(forecast_weather, self.__fields_for_fetch[0], None)
            else None
        )
        return weather
