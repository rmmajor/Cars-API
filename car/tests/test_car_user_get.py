import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from user.tests.factories import *
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from car.factories import CarFactory
from brand.factories import BrandFactory
from model.factories import ModelFactory


@pytest.mark.django_db
class TestBrandGet:

    def _register_user(self):
        self.user = UserFactory.create()
        self.user.set_password('defaultpassword')
        self.user.save()

        self.username = self.user.username
        self.password = 'defaultpassword'

        return RefreshToken.for_user(self.user)

    def _login(self, refresh_token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')
        self.client.login(username=self.username, password=self.password)

    def _generate_brands(self, count):
        return BrandFactory.create_batch(count)

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        refresh_token = self._register_user()
        self._login(refresh_token)
        self.url = 'http://127.0.0.1:8000/brands/'

