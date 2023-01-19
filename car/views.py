from rest_framework import viewsets, permissions
from .serializers import CarSerializer
from .models import Car
from django_filters import rest_framework as filters
from .filters import CarYearFilter


class CarAllViewSet(viewsets.ModelViewSet):
    """"Displayes all cars in database"""

    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer
    # permission_classes = None # todo: change later

    # for filtering like /brands/?headquarters_country=Germany&brand_name=BMW
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id', 'brand', 'model', 'price', 'milage',
                        'exterior_color', 'interior_color', 'fuel_type',
                        'transmission', 'engine', 'is_on_sale')
    filterset_class = CarYearFilter


class CarViewSet(viewsets.ModelViewSet):
    """"Displays only cars for sale"""

    queryset = Car.objects.filter(is_on_sale=True).order_by('id')
    serializer_class = CarSerializer
    # permission_classes = None # todo: change later

    # for filtering like /brands/?headquarters_country=Germany&brand_name=BMW
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id', 'brand', 'model', 'price', 'milage',
                        'exterior_color', 'interior_color', 'fuel_type',
                        'transmission', 'engine', 'is_on_sale')
    filterset_class = CarYearFilter
