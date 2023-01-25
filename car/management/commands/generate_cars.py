from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from car.models import Car
from brand.models import Brand
from model.models import Model
from car.factories import CarFactory
import random

"""
This file implements manage.py console command: 
    python manage.py generate_models <count>

go: https://docs.djangoproject.com/en/3.2/howto/custom-management-commands/
"""

FUEL_TYPE_OPTIONS = ['Gasoline', 'Diesel Fuel', 'Bio-diesel', 'Ethanol', 'Electric']
TRANSMISSION_OPTIONS = ['Manual', 'Automatic', 'CVT']
ENGINE_OPTIONS = ['2.0L', '1.4L', '3.0L', '5.0L']


class Command(BaseCommand):

    # this attribute sets output for --help flag of the command
    help = 'Generates records for Car instance'

    def add_arguments(self, parser):
        parser.add_argument('count', action='store', nargs='+', type=int)

    def handle(self, *args, **options):

        count = options['count'][0]
        # generate_fake_model_records(count)

        car_records = CarFactory.create_batch(count)
        return self.stdout.write("done")


def generate_fake_model_records(count):
    fake = Faker()
    Faker.seed(123)
    fake.add_provider(VehicleProvider)

    for _ in range(count):
        brand_instance = random.choice(Brand.objects.all())
        model_instance = random.choice(Model.objects.all())
        price = random.randint(0, 5000000)
        milage = random.randint(0, 5000000)
        exterior_color = fake.color_name()
        interior_color = fake.color_name()
        fuel_type = random.choice(FUEL_TYPE_OPTIONS)
        transmission = random.choice(TRANSMISSION_OPTIONS)
        engine = random.choice(ENGINE_OPTIONS)
        is_on_sale = bool(random.getrandbits(1))  # gens True or False randomly

        insert_fake_model_record(brand_instance, model_instance, price, milage, exterior_color, interior_color,
                                 fuel_type, transmission, engine, is_on_sale)

        print(_, brand_instance, model_instance, price, milage, exterior_color, interior_color,
              fuel_type, transmission, engine, is_on_sale)  # temp line


def insert_fake_model_record(brand_instance, model_instance, price, milage, exterior_color, interior_color,
                             fuel_type, transmission, engine, is_on_sale):
    model = Car()
    model.brand = brand_instance
    model.model = model_instance
    model.price = price
    model.milage = milage
    model.exterior_color = exterior_color
    model.interior_color = interior_color
    model.fuel_type = fuel_type
    model.transmission = transmission
    model.engine = engine
    model.is_on_sale = is_on_sale

    model.save()
