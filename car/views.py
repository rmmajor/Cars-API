from rest_framework import viewsets, permissions
from .serializers import CarSerializer
from .models import Car
from django_filters import rest_framework as filters


class CarViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all().order_by('id')
    serializer_class = CarSerializer
    # permission_classes = None # todo: change later

    # for filtering like /brands/?headquarters_country=Germany&brand_name=BMW
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id', 'brand', 'model', 'price', 'milage',
                        'exterior_color', 'interior_color', 'fuel_type',
                        'transmission', 'engine', 'is_on_sale')
