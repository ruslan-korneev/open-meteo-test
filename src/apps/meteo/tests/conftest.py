import factory
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

    temperature_2m_max = factory.Faker("pyfloat", positive=True, max_value=100)
    temperature_2m_min = factory.Faker("pyfloat", positive=True, max_value=100)
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
