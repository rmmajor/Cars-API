from django_filters import rest_framework as filters
from .models import Brand

"""
!This file is not used in code!

Its a custom filter class, and as far as i anderstood, if all you need is simple filtering, you don't have to 
make this file
"""


class BrandFilter(filters.FilterSet):

    class Meta:
        model = Brand
        fields = ['brand_name', 'headquarters_country']

