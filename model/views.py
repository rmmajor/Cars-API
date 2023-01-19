from rest_framework import viewsets, permissions
from .serializers import ModelSerializer
from .models import Model
from django_filters import rest_framework as filters


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all().order_by('id')
    serializer_class = ModelSerializer
    # permission_classes = None # todo: change later

    # for filtering like /brands/?headquarters_country=Germany&brand_name=BMW
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('model_name', 'issue_year', 'body_style')
