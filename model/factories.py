import factory
from faker import Faker
from faker_vehicle import VehicleProvider
from factory.django import DjangoModelFactory
import time
from .models import *

fake = Faker()
Faker.seed(time.time() * 1000)
fake.add_provider(VehicleProvider)


class ModelFactory(DjangoModelFactory):
    class Meta:
        model = Model

    model_name = factory.LazyAttribute(lambda obj: fake.vehicle_model())
    issue_year = factory.LazyAttribute(lambda obj: fake.vehicle_year())
    body_style = factory.LazyAttribute(lambda obj: fake.vehicle_category())
