# Generated by Django 4.1.5 on 2023-01-19 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("model", "0001_initial"),
        ("brand", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.IntegerField()),
                ("milage", models.IntegerField()),
                ("exterior_color", models.CharField(max_length=30)),
                ("interior_color", models.CharField(max_length=30)),
                ("fuel_type", models.CharField(max_length=30)),
                (
                    "transmission",
                    models.CharField(
                        choices=[
                            ("Manual", "Manual"),
                            ("Automatic", "Automatic"),
                            ("CVT", "CVT"),
                        ],
                        default="Manual",
                        max_length=100,
                    ),
                ),
                ("engine", models.CharField(max_length=10)),
                ("is_on_sale", models.BooleanField()),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="brand.brand"
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="model.model"
                    ),
                ),
            ],
            options={
                "ordering": ["price"],
            },
        ),
    ]
