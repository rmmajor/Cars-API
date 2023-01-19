from django.db import models


# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length=60)
    headquarters_country = models.CharField(max_length=150)

    def __str__(self):
        return self.brand_name

    class Meta:
        ordering = ['brand_name']
        verbose_name = "brand"
        verbose_name_plural = "brands"
