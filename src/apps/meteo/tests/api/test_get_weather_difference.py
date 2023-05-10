import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_weather_difference_without_city(client: APIClient):
    response = client.get(reverse("weather-difference"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.data


@pytest.mark.django_db
def test_get_weather_difference_with_city(client: APIClient, city, weather):
    response = client.get(reverse("weather-difference"), {"city": city.name})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data