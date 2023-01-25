from rest_framework import serializers
from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "brand_name", "headquarters_country"]
