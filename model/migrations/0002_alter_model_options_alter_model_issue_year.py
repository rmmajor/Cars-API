# Generated by Django 4.1.5 on 2023-01-19 19:15

from django.db import migrations, models
import model.validators


class Migration(migrations.Migration):

    dependencies = [
        ("model", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="model",
            options={
                "ordering": ["model_name"],
                "verbose_name": "model",
                "verbose_name_plural": "models",
            },
        ),
        migrations.AlterField(
            model_name="model",
            name="issue_year",
            field=models.IntegerField(validators=[model.validators.validate_year]),
        ),
    ]
