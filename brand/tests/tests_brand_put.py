import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework_simplejwt.tokens import RefreshToken
from ..factories import *
from user.tests.factories import *
from rest_framework import status
from rest_framework.test import APIClient

"""
For unknown reasons, this test work perfectly apart from each other, 
but fail together
"""


@pytest.mark.django_db
class TestBrandPUTbyAdmin:
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
        self.brand_detail_url = "http://127.0.0.1:8000/brands/1/"
        self.brand_to_put = factory.build(dict, FACTORY_CLASS=BrandFactory)
        self.brand_records = BrandFactory.create_batch(5)

    def test_put_success(self):

        response = self.client.put(self.brand_detail_url, self.brand_to_put)
        assert response.status_code == status.HTTP_200_OK
        
    def test_put_without_fields(self):
        for key, value in self.brand_to_put.items():
            bad_brand = self.brand_to_put.copy()
            bad_brand.pop(key)
            response = self.client.put(self.brand_detail_url, bad_brand)

            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_with_empty_fields(self):
        for key, value in self.brand_to_put.items():
            bad_brand = self.brand_to_put.copy()
            bad_brand[key] = ""
            response = self.client.put(self.brand_detail_url, bad_brand)

            assert response.status_code == status.HTTP_400_BAD_REQUEST
