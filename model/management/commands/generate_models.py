from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from model.models import Model
from model.factories import ModelFactory

"""
This file implements manage.py console command: 
    python manage.py generate_models <count>

go: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
"""


class Command(BaseCommand):

    # this attribute sets output for --help flag of the command
    help = "Generates records for Model instance"

    def add_arguments(self, parser):
        parser.add_argument("count", action="store", nargs="+", type=int)

    def handle(self, *args, **options):
        count = options["count"][0]
        model_records = ModelFactory.create_batch(count)
        return self.stdout.write("done")
