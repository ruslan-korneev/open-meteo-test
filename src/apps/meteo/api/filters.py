from django_filters import DateFilter, CharFilter, FilterSet

from src.apps.meteo.models.weather import Weather


class WeatherFilterSet(FilterSet):
    city = CharFilter(field_name="city__name", lookup_expr="iexact", required=True)
    start_date = DateFilter(field_name="date", lookup_expr="gte")
    end_date = DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Weather
        fields = ("city", "start_date", "end_date")
