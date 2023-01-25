from rest_framework import viewsets
from .serializers import ModelSerializer
from .models import Model
from django_filters import rest_framework as filters
from .filters import ModelFilter
from Core.acces_policy import DefaultAccessPolicy


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all().order_by("id")
    serializer_class = ModelSerializer
    permission_classes = [DefaultAccessPolicy]

    # for filtering like /brands/?headquarters_country=Germany&brand_name=BMW
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ModelFilter
