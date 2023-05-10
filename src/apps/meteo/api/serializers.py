from rest_framework import serializers

from src.apps.meteo.models.weather import Weather, WeatherData


class GetWeatherSerializer(serializers.Serializer):
    city_name = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError(
                {"start_date": "Start date cannot be greater than end date."}
            )

        return attrs


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = (
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
        )


class WeatherSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=100, source="city.name")
    forecast = WeatherDataSerializer()
    measured = WeatherDataSerializer()

    class Meta:
        model = Weather
        fields = ("city", "date", "measured", "forecast")


class ForecastMeasuredDifferenceSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=100, source="city.name")
    temperature_2m_max_diff = serializers.SerializerMethodField()
    temperature_2m_min_diff = serializers.SerializerMethodField()
    precipitation_sum_diff = serializers.SerializerMethodField()
    windspeed_10m_max_diff = serializers.SerializerMethodField()

    class Meta:
        model = Weather
        fields = (
            "city",
            "date",
            "temperature_2m_max_diff",
            "temperature_2m_min_diff",
            "precipitation_sum_diff",
            "windspeed_10m_max_diff",
        )

    def get_temperature_2m_max_diff(self, obj):
        if not obj.measured or not obj.forecast:
            return None
        return abs(obj.forecast.temperature_2m_max - obj.measured.temperature_2m_max)

    def get_temperature_2m_min_diff(self, obj):
        if not obj.measured or not obj.forecast:
            return None
        return abs(obj.forecast.temperature_2m_min - obj.measured.temperature_2m_min)

    def get_precipitation_sum_diff(self, obj):
        if not obj.measured or not obj.forecast:
            return None
        return abs(obj.forecast.precipitation_sum - obj.measured.precipitation_sum)

    def get_windspeed_10m_max_diff(self, obj):
        if not obj.measured or not obj.forecast:
            return None
        return abs(obj.forecast.windspeed_10m_max - obj.measured.windspeed_10m_max)
