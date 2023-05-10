from datetime import timedelta

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_weather_without_city(client):
    """
    Test get weather without city
    city parameter is required
    """
    response = client.get(reverse("weather-list"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_weather_with_city(client: APIClient, city, weather):
    response = client.get(reverse("weather-list"), {"city": city.name})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data

    # case insensitive
    response = client.get(reverse("weather-list"), {"city": city.name.upper()})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data

    # no city with that name, should return empty list
    response = client.get(reverse("weather-list"), {"city": f"{city.name}F"})
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 0, response.data


@pytest.mark.django_db
def test_get_weather_with_city_and_date(client: APIClient, city, weather):
    # start date equal to weather date
    response = client.get(
        reverse("weather-list"), {"city": city.name, "start_date": weather.date}
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data

    # end date equal to weather date
    response = client.get(
        reverse("weather-list"), {"city": city.name, "end_date": weather.date}
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data

    # start date and end date equal to weather date
    response = client.get(
        reverse("weather-list"),
        {"city": city.name, "start_date": weather.date, "end_date": weather.date},
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 1, response.data

    # end date before weather date
    response = client.get(
        reverse("weather-list"),
        {"city": city.name, "end_date": weather.date - timedelta(days=1)},
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 0, response.data

    # start date after weather date
    response = client.get(
        reverse("weather-list"),
        {"city": city.name, "start_date": weather.date + timedelta(days=1)},
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    assert len(response.data) == 0, response.data
