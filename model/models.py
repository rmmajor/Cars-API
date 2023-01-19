from django.db import models


# Create your models here.
class Model(models.Model):
    model_name = models.CharField(max_length=60)
    issue_year = models.IntegerField()  # todo check if there is a type for years
    body_style = models.CharField(max_length=60)

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['model_name']