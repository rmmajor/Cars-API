import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from brand.factories import BrandFactory
from car.factories import CarFactory
from model.factories import ModelFactory
from user.tests.factories import *
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBrandDELETEbyAdmin:

    def _register_admin(self):
        self.admin = UserFactory.create(is_superuser=True)
        self.admin.set_password('password')
        self.admin.save()

        self.username = self.admin.username
        self.password = 'password'

        return RefreshToken.for_user(self.admin)

    def _login(self, refresh_token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')
        self.client.login(username=self.username, password=self.password)

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        admin_token = self._register_admin()
        self._login(admin_token)
        self.car_detail_url = 'http://127.0.0.1:8000/cars/1/'

        self.brands_records = BrandFactory.create_batch(5)
        self.models_records = ModelFactory.create_batch(5)

        self.car_to_delete = CarFactory.create_batch(5,
                                                     brand=self.brands_records[0],
                                                     model=self.models_records[0],
                                                     is_on_sale=True)

    def test_delete_car_success(self):
        delete_response = self.client.delete(self.car_detail_url)
        get_response = self.client.get(self.car_detail_url)

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_non_existing_car(self):
        url = reverse("brand-detail", args=(404,))
        delete_response = self.client.delete(url)

        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
