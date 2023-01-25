import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = "testtest"
    email = "testtest@mail.test"
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    is_active = True
    is_superuser = False
    is_staff = False
