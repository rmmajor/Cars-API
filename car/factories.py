import factory
from faker import Faker
from faker_vehicle import VehicleProvider
from factory.django import DjangoModelFactory
from faker.providers import DynamicProvider
import time
from .models import *

fuel_type_provider = DynamicProvider(
     provider_name="fuel_type",
     elements=['Gasoline', 'Diesel Fuel', 'Bio-diesel', 'Ethanol', 'Electric']
)


transmission_provider = DynamicProvider(
     provider_name="transmission",
     elements=['Manual', 'Automatic', 'CVT']
)


engine_provider = DynamicProvider(
     provider_name="engine",
     elements=['2.0L', '1.4L', '3.0L', '5.0L']
)

fake = Faker()
Faker.seed(time.time() * 1000)
fake.add_provider(VehicleProvider)

# my providers
fake.add_provider(fuel_type_provider)
fake.add_provider(transmission_provider)
fake.add_provider(engine_provider)


class CarFactory(DjangoModelFactory):

    class Meta:
        model = Car

    brand = factory.Iterator(Brand.objects.all())
    model = factory.Iterator(Model.objects.all())
    price = factory.LazyAttribute(lambda obj: fake.pyint())
    milage = factory.LazyAttribute(lambda obj: fake.pyint())
    exterior_color = factory.LazyAttribute(lambda obj: fake.color_name())
    interior_color = factory.LazyAttribute(lambda obj: fake.color_name())
    fuel_type = factory.LazyAttribute(lambda obj: fake.fuel_type())
    transmission = factory.LazyAttribute(lambda obj: fake.transmission())
    engine = factory.LazyAttribute(lambda obj: fake.engine())
    is_on_sale = factory.LazyAttribute(lambda obj: fake.pybool())
