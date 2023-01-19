from django_filters import rest_framework as filters
from django_filters import RangeFilter
from .models import Model


class ModelYearOfIssueFilter(filters.FilterSet):
    """
    Will manage queries like `GET /models/?year_min=2010&year_max=2021`
    """
    year = RangeFilter(field_name='issue_year')

    class Meta:
        model = Model
        fields = ['issue_year']
