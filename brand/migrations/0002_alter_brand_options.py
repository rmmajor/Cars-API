# Generated by Django 4.1.5 on 2023-01-19 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("brand", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="brand",
            options={
                "ordering": ["brand_name"],
                "verbose_name": "brand",
                "verbose_name_plural": "brands",
            },
        ),
    ]
