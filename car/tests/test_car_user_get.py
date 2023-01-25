import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from user.tests.factories import *
from car.factories import CarFactory
from brand.factories import BrandFactory
from model.factories import ModelFactory


@pytest.mark.django_db
class TestCarGet:

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

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        refresh_token = self._register_user()
        self._login(refresh_token)
        self.url = 'http://127.0.0.1:8000/cars/'

        self.brands_records = BrandFactory.create_batch(5)
        self.models_records = ModelFactory.create_batch(5)
        # self.car_records  = CarFactory.create_batch(5)

    def test_cars_list_success(self):
        response = self.client.get(self.url)
        # print(response.data)
        assert response.status_code == status.HTTP_200_OK

    def test_get_car_detail_success(self):
        car_records = CarFactory.create_batch(5)
        url = reverse("car-detail", args=(1,))
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_non_existing_instance_detail(self):
        brand_id = 1
        url = reverse("car-detail", args=(brand_id,))
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_cars_empty_set(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_cars_without_credentials(self, client):
        response = client.get(self.url)
        expected_response = {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                   code='not_authenticated')}

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == expected_response

    @pytest.mark.parametrize(
        "filters",
        ['?fuel_type=Gasoline',
         '?transmission=Manual&year_min=2019',
         '?transmission=Manual&year_min=2000&year_max=2022',
         '?exterior_color=DarkCyan']
    )
    def test_get_cars_with_filters(self, filters):
        cars_records = CarFactory.create_batch(5, brand=self.brands_records[0], model=self.models_records[0])
        url = 'http://127.0.0.1:8000/cars/'
        response = self.client.get(url + filters)

        assert response.status_code == status.HTTP_200_OK
