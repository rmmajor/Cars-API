import factory
from faker import Faker
from faker_vehicle import VehicleProvider
from factory.django import DjangoModelFactory
import time
from .models import *

fake = Faker()
Faker.seed(time.time() * 1000)
fake.add_provider(VehicleProvider)


class BrandFactory(DjangoModelFactory):
    class Meta:
        model = Brand

    brand_name = factory.LazyAttribute(lambda obj: fake.vehicle_make())
    headquarters_country = factory.LazyAttribute(lambda obj: fake.country())
