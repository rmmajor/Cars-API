from django.db import models
from brand.models import Brand
from model.models import Model
from .validators import validate_nonnegative

TRANSMISSION_OPTIONS = (
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic'),
    ('CVT', 'CVT')
)


# Create your models here.
class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[validate_nonnegative])
    milage = models.IntegerField(validators=[validate_nonnegative])
    exterior_color = models.CharField(max_length=30)
    interior_color = models.CharField(max_length=30)
    fuel_type = models.CharField(max_length=30)
    transmission = models.CharField(choices=TRANSMISSION_OPTIONS, default='Manual', max_length=100)
    engine = models.CharField(max_length=10)
    is_on_sale = models.BooleanField()

    def __str__(self):
        return "%s %s" % (self.brand.brand_name, self.model.model_name)

    class Meta:
        ordering = ['price']
        verbose_name = "car"
        verbose_name_plural = "cars"
