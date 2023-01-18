from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import BrandSerializer
from .models import Brand


# Create your views here.
class BrandViewSet(viewsets.ModelViewSet):

    queryset = Brand.objects.all().order_by('id')
    serializer_class = BrandSerializer
    # permission_classes = None # todo: change later



