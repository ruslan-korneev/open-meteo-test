import io

import pytest
from django.core.management import call_command


class TestWeatherCommandFailure:
    def call_command(self, *args, **kwargs) -> str:
        out = io.StringIO()
        with pytest.raises(SystemExit):
            call_command("weather", *args, **kwargs, stdout=out)
        return out.getvalue()

    @pytest.mark.django_db
    def test_get_weather_with_wrong_date_format(self):
        response = self.call_command("Warsaw", "2020-00-00", "09-03-3")
        assert "Date has wrong format" in response, response

    @pytest.mark.django_db
    def test_get_weather_with_wrong_date(self):
        response = self.call_command("Warsaw", "2020-01-02", "2020-01-01")
        assert "Start date cannot be greater than end date." in response, response

    @pytest.mark.django_db
    def test_get_weather_with_wrong_city(self, mock_requests):
        mock_requests.get.return_value.status_code = 404
        city_name = "1"
        response = self.call_command(city_name, "2020-01-01", "2020-01-02")
        assert (
            f"City {city_name} does not exist in OpenMeteo GEO API." in response
        ), response


class TestWeatherCommandSuccess:
    def call_command(self, *args, **kwargs) -> str:
        out = io.StringIO()
        call_command("weather", *args, **kwargs, stdout=out)
        return out.getvalue()

    @pytest.mark.django_db
    def test_get_weather_with_city_and_date(
        self, mock_open_meteo_requests, settings, mocker
    ):
        mock_save_in_file = mocker.patch(
            "src.apps.meteo.management.commands.weather.Command.save_weather_data",
        )
        mock_save_in_file.side_effect = (
            lambda data, output: f"weather_data_{data[0].city.name}_{data[0].date}_{data[-1].date}.{output}"
        )
        response = self.call_command("London", "2020-01-01", "2020-01-02")
        assert "Weather data has been downloaded successfully" in response, response
