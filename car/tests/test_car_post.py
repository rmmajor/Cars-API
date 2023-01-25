import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework_simplejwt.tokens import RefreshToken

from brand.factories import BrandFactory
from model.factories import ModelFactory
from user.tests.factories import *
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCarPOSTbyAdmin:
    def _register_admin(self):
        self.admin = UserFactory.create(is_superuser=True)
        self.admin.set_password("password")
        self.admin.save()

        self.username = self.admin.username
        self.password = "password"

        return RefreshToken.for_user(self.admin)

    def _login(self, refresh_token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh_token.access_token}"
        )
        self.client.login(username=self.username, password=self.password)

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        admin_token = self._register_admin()
        self._login(admin_token)
        self.car_list_url = "http://127.0.0.1:8000/cars/"

        self.brands_records = BrandFactory.create_batch(5)
        self.models_records = ModelFactory.create_batch(5)
        self.car_to_post = {
            "brand": 1,
            "model": 3,
            "price": 1000000000,
            "milage": 1000000,
            "exterior_color": "blue",
            "interior_color": "yellow",
            "fuel_type": "gas",
            "transmission": "Manual",
            "engine": "2.0L",
            "is_on_sale": True,
        }

    def test_post_success(self):
        response = self.client.post(self.car_list_url, self.car_to_post)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_without_fields(self):
        """
        Checking if each field is required.
        Fields that can be dropped from the request are transmission (because it has
        default value 'Manual') and is_on_sale (because bool default value is False)
        """
        for key, value in self.car_to_post.items():
            bad_car = self.car_to_post.copy()
            bad_car.pop(key)
            response = self.client.post(self.car_list_url, bad_car)

            if key == 'transmission' or key == 'is_on_sale':
                assert response.status_code == status.HTTP_201_CREATED
            else:
                assert response.data[key] == [ErrorDetail(string='This field is required.', code='required')]
                assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_transmission(self):
        bad_car = self.car_to_post
        bad_car["transmission"] = ""
        response = self.client.post(self.car_list_url, bad_car)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_negative_price(self):
        bad_car = self.car_to_post
        bad_car["price"] = -400
        response = self.client.post(self.car_list_url, bad_car)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_negative_milage(self):
        bad_car = self.car_to_post
        bad_car["milage"] = -400
        response = self.client.post(self.car_list_url, bad_car)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
