from unittest.mock import Mock

import factory
import pytest
from pytest_factoryboy import register

from src.apps.meteo.models.cities import City
from src.apps.meteo.models.weather import Weather, WeatherData


@register
class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Faker("city")
    latitude = factory.Faker("pyfloat", min_value=-90, max_value=90)
    longitude = factory.Faker("pyfloat", min_value=-180, max_value=180)


@register
class WeatherDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeatherData

    temperature_2m_max = factory.Faker(
        "pyfloat", positive=True, min_value=50, max_value=100
    )
    temperature_2m_min = factory.Faker("pyfloat", positive=True, max_value=50)
    precipitation_sum = factory.Faker("pyfloat", positive=True, max_value=100)
    windspeed_10m_max = factory.Faker("pyfloat", positive=True, max_value=100)


@register
class WeatherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Weather

    city = factory.SubFactory(CityFactory)
    date = factory.Faker("date_object")
    measured = factory.SubFactory(WeatherDataFactory)
    forecast = factory.SubFactory(WeatherDataFactory)


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch("requests.get")


@pytest.fixture
def mock_open_meteo_responses(settings):
    return {
        f"{settings.OPEN_METEO_API}forecast": {
            "status_code": 200,
            "json_data": {
                "latitude": 51.5,
                "longitude": -0.120000124,
                "generationtime_ms": 1.5898942947387695,
                "utc_offset_seconds": 3600,
                "timezone": "Europe/London",
                "timezone_abbreviation": "BST",
                "elevation": 29.0,
                "daily_units": {
                    "time": "iso8601",
                    "temperature_2m_max": "°C",
                    "temperature_2m_min": "°C",
                    "precipitation_sum": "mm",
                    "windspeed_10m_max": "km/h",
                },
                "daily": {
                    "time": ["2023-05-01", "2023-05-02"],
                    "temperature_2m_max": [17.5, 14.3],
                    "temperature_2m_min": [10.2, 8.6],
                    "precipitation_sum": [0.30, 0.00],
                    "windspeed_10m_max": [14.4, 14.4],
                },
            },
        },
        f"{settings.OPEN_METEO_HISTORICAL_API}archive": {
            "status_code": 200,
            "json_data": {
                "latitude": 51.5,
                "longitude": -0.099990845,
                "generationtime_ms": 1.2549161911010742,
                "utc_offset_seconds": 3600,
                "timezone": "Europe/London",
                "timezone_abbreviation": "BST",
                "elevation": 29.0,
                "daily_units": {
                    "time": "iso8601",
                    "temperature_2m_max": "°C",
                    "temperature_2m_min": "°C",
                    "precipitation_sum": "mm",
                    "windspeed_10m_max": "km/h",
                },
                "daily": {
                    "time": ["2023-05-01", "2023-05-02"],
                    "temperature_2m_max": [16.7, 13.0],
                    "temperature_2m_min": [8.1, 7.9],
                    "precipitation_sum": [3.90, 0.00],
                    "windspeed_10m_max": [14.5, 14.4],
                },
            },
        },
        f"{settings.OPEN_METEO_GEO_API}search": {
            "status_code": 200,
            "json_data": {
                "results": [
                    {
                        "id": 2643743,
                        "name": "London",
                        "latitude": 51.50853,
                        "longitude": -0.12574,
                        "elevation": 25.0,
                        "feature_code": "PPLC",
                        "country_code": "GB",
                        "admin1_id": 6269131,
                        "admin2_id": 2648110,
                        "timezone": "Europe/London",
                        "population": 7556900,
                        "country_id": 2635167,
                        "country": "United Kingdom",
                        "admin1": "England",
                        "admin2": "Greater London",
                    }
                ],
                "generationtime_ms": 0.6340742,
            },
        },
    }


@pytest.fixture
def mock_open_meteo_requests(mock_requests, mock_open_meteo_responses):
    def mock_get(url, *args, **kwargs):
        response = Mock()
        if url in mock_open_meteo_responses:
            mock_data = mock_open_meteo_responses[url]
            response.status_code = mock_data["status_code"]
            response.json.return_value = mock_data["json_data"]
        else:
            assert False, f"Unknown URL: {url}"
            response.status_code = 500  # Set a default status code for unknown URLs
        return response

    mock_requests.side_effect = mock_get
    return mock_requests
