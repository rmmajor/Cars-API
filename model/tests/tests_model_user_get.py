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
        self.user.set_password("defaultpassword")
        self.user.save()

        self.username = self.user.username
        self.password = "defaultpassword"

        return RefreshToken.for_user(self.user)

    def _login(self, refresh_token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh_token.access_token}"
        )
        self.client.login(username=self.username, password=self.password)

    def _generate_models(self, count):
        return ModelFactory.create_batch(count)

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        refresh_token = self._register_user()
        self._login(refresh_token)
        self.url = "http://127.0.0.1:8000/models/"

    def test_get_models_list_success(self):
        model_records = self._generate_models(5)
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_model_detail_success(self):
        model_records = self._generate_models(5)
        model_id = 2
        url = reverse("model-detail", args=(model_id,))
        response = self.client.get(url)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK

    def test_get_non_existing_instance_detail(self):
        brand_id = 1
        url = reverse("brand-detail", args=(brand_id,))
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_models_empty_set(self):
        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == []

    def test_get_models_without_credentials(self, client):
        response = client.get(self.url)
        expected_response = {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == expected_response

    def test_get_models_with_model_name_filter(self):
        model_records = self._generate_models(5)
        response = self.client.get("http://127.0.0.1:8000/models/?model_name=X5")
        assert response.status_code == status.HTTP_200_OK

    def test_get_models_with_issue_year_filter(self):
        model_records = self._generate_models(5)
        response = self.client.get("http://127.0.0.1:8000/models/?issue_year=2008")

        assert response.status_code == status.HTTP_200_OK

    def test_get_models_with_body_style_filter(self):
        model_records = self._generate_models(5)
        response = self.client.get("http://127.0.0.1:8000/models/?body_style=sedan")

        assert response.status_code == status.HTTP_200_OK

    def test_get_models_with_year_range_filter(self):
        model_records = self._generate_models(5)
        response = self.client.get(
            "http://127.0.0.1:8000/models/?year_min=1900&year_max=2020"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_get_models_with_min_year_filter(self):
        model_records = self._generate_models(5)
        response = self.client.get("http://127.0.0.1:8000/models/?year_min=1900")

        assert response.status_code == status.HTTP_200_OK

    def test_get_models_with_max_year_filter(self):
        model_records = self._generate_models(5)
        response = self.client.get("http://127.0.0.1:8000/models/?year_max=2020")

        assert response.status_code == status.HTTP_200_OK

    def test_get_models_with_mixed_filters(self):
        brand_records = self._generate_models(5)
        response = self.client.get(
            "http://127.0.0.1:8000/brands/"
            "?model_name=X5&"
            "issue_year=2008&"
            "body_style=sedan"
        )

        assert response.status_code == status.HTTP_200_OK
