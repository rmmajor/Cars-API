from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from model.models import Model

"""
This file implements manage.py console command: 
    python manage.py generate_models <count>

go: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
"""


class Command(BaseCommand):

    # this attribute sets output for --help flag of the command
    help = 'Generates records for Model instance'

    def add_arguments(self, parser):
        parser.add_argument('count', action='store', nargs='+', type=int)

    def handle(self, *args, **options):

        count = options['count'][0]
        generate_fake_model_records(count)

        return self.stdout.write("test")


def generate_fake_model_records(count):
    fake = Faker()
    Faker.seed(123)
    fake.add_provider(VehicleProvider)

    for _ in range(count):
        model_name = fake.vehicle_model()
        issue_year = fake.vehicle_year()
        body_style = fake.vehicle_category()

        insert_fake_model_record(model_name, issue_year, body_style)
        print(_, model_name, issue_year, body_style)  # temp line


def insert_fake_model_record(model_name, issue_year, body_style):
    model = Model()
    model.model_name = model_name
    model.issue_year = issue_year
    model.body_style = body_style
    model.save()
