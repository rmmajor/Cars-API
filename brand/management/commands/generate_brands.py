from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from brand.models import Brand

"""
This file implements manage.py console command: 
    python manage.py generate_brands <count>

go: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
"""


class Command(BaseCommand):

    # this attribute sets output for --help flag of the command
    help = 'Generates records for Brand instance'

    def add_arguments(self, parser):
        parser.add_argument('count', action='store', nargs='+', type=int)

    def handle(self, *args, **options):

        count = options['count'][0]
        generate_fake_brand_records(count)

        return self.stdout.write("test")


def generate_fake_brand_records(count):
    fake = Faker()
    Faker.seed(123)
    fake.add_provider(VehicleProvider)

    for _ in range(count):
        brand_name = fake.vehicle_make()
        headquarters_country = fake.country()
        insert_fake_brand_record(brand_name, headquarters_country)
        print(_, brand_name, headquarters_country)  # temp line


def insert_fake_brand_record(brand_name, headquarters_country):
    brand = Brand()
    brand.brand_name = brand_name
    brand.headquarters_country = headquarters_country
    brand.save()
