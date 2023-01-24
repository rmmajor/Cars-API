import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from ..factories import *
from user.tests.factories import *
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from django.urls import reverse


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

    def test_get_brands_list_success(self):
        brand_records = self._generate_brands(5)
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    # does not work
    def test_get_brand_detail_success(self, client):
        brand_records = self._generate_brands(5)
        brand_id = 1
        response = self.client.get(f'http://127.0.0.1:8000/brands/{brand_id}')
        print(response)
        assert response.status_code == status.HTTP_200_OK

    def test_get_brands_empty_set(self, client):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_brands_without_credentials(self, client):
        response = client.get(self.url)
        expected_response = {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                   code='not_authenticated')}

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == expected_response

    def test_get_brands_with_brand_name_filter(self):
        brand_records = self._generate_brands(5)
        response = self.client.get('http://127.0.0.1:8000/brands/?brand_name=BMW')
        assert response.status_code == status.HTTP_200_OK

    def test_get_brands_with_headquarters_country_filter(self):
        brand_records = self._generate_brands(5)
        response = self.client.get('http://127.0.0.1:8000/brands/?headquarters_country=Ukraine')

        assert response.status_code == status.HTTP_200_OK

    def test_get_brands_with_headquarters_mixed_filters(self):
        brand_records = self._generate_brands(5)
        response = self.client.get('http://127.0.0.1:8000/brands/'
                                   '?headquarters_country=Ukraine&'
                                   'brand_name=BMW')

        assert response.status_code == status.HTTP_200_OK


class TestBrandCRUDbyAdmin:
    pass
