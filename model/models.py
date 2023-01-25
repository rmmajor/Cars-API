from django.db import models
from .validators import validate_year


# Create your models here.
class Model(models.Model):
    model_name = models.CharField(max_length=60)
    issue_year = models.IntegerField(validators=[validate_year])
    body_style = models.CharField(max_length=60)

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ["model_name"]
        verbose_name = "model"
        verbose_name_plural = "models"
