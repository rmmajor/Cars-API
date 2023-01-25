import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from ..factories import *
from user.tests.factories import *
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestBrandPOSTbyAdmin:
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
        self.brand_list_url = "http://127.0.0.1:8000/brands/"
        self.brand_to_post = factory.build(dict, FACTORY_CLASS=BrandFactory)
        self.brand_records = BrandFactory.create_batch(5)

    def test_post_success(self):
        response = self.client.post(self.brand_list_url, self.brand_to_post)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_without_brand_name(self):
        bad_brand = self.brand_to_post
        bad_brand.pop("brand_name")
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_without_headquarters_country(self):
        bad_brand = self.brand_to_post
        bad_brand.pop("headquarters_country")
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_brand_name(self):
        bad_brand = self.brand_to_post
        bad_brand["brand_name"] = ""
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_headquarters_country(self):
        bad_brand = self.brand_to_post
        bad_brand["headquarters_country"] = ""
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
