from django_filters import rest_framework as filters
from django_filters import RangeFilter
from .models import Model


class ModelFilter(filters.FilterSet):
    year = RangeFilter(field_name='issue_year')

    class Meta:
        model = Model
        fields = ['issue_year', "model_name", "body_style"]
