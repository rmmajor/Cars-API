from django_filters import rest_framework as filters
from django_filters import RangeFilter
from .models import Car


class CarYearFilter(filters.FilterSet):
    """
    Will manage queries like `GET /cars/?year_min=2010&year_max=2021`
    """

    year = RangeFilter(field_name="model__issue_year")

    class Meta:
        model = Car
        fields = [
            "model__issue_year",
            "id",
            "brand",
            "model",
            "price",
            "milage",
            "exterior_color",
            "interior_color",
            "fuel_type",
            "transmission",
            "engine",
            "is_on_sale",
        ]
