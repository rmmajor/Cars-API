from rest_framework import serializers
from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'price', 'milage',
                  'exterior_color', 'interior_color', 'fuel_type',
                  'transmission', 'engine', 'is_on_sale']
