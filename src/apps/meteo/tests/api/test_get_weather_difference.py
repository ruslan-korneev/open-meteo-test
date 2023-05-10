import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from src.apps.meteo.models.weather import Weather


@pytest.mark.django_db
def test_get_weather_difference_without_city(client: APIClient):
    """
    Test get weather difference without city, should return 400, city is required
    """
    response = client.get(reverse("weather-difference"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data


@pytest.mark.django_db
def test_get_weather_difference_with_measured_weather_data_only(
    client: APIClient, weather: Weather
):
    """Looking for weather with both measured and forecast data, so this should return empty list"""
    weather.forecast = None
    weather.save()
    response = client.get(reverse("weather-difference"), {"city": weather.city.name})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 0, response.data


@pytest.mark.django_db
def test_get_weather_difference_with_measured_and_forecast_weather_data(
    client: APIClient, weather, weather_data_factory
):
    """
    Success case for weather with both measured and forecast data
    """
    first_weather_data = weather_data_factory()
    second_weather_data = weather_data_factory()
    weather.measured = first_weather_data
    weather.forecast = second_weather_data
    weather.save()
    response = client.get(reverse("weather-difference"), {"city": weather.city.name})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data
    response_data = response.data[0]
    assert response_data["city"] == weather.city.name, response_data
    assert response_data["date"] == weather.date.strftime("%Y-%m-%d"), response_data
    assert float(response_data["temperature_2m_max_diff"]) == round(
        abs(weather.measured.temperature_2m_max - weather.forecast.temperature_2m_max),
        2,
    ), response_data
