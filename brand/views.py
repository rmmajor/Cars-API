from rest_framework import viewsets, permissions
from .serializers import BrandSerializer
from .models import Brand
from django_filters import rest_framework as filters


class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
    # permission_classes = None # todo: change later

    # for filtering like /brands/?headquarters_country=Germany&brand_name=BMW
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('brand_name', 'headquarters_country')
