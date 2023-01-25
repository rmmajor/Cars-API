import pytest
from .factories import *
from rest_framework import status
from rest_framework.exceptions import ErrorDetail


@pytest.mark.django_db
class TestLoginUser:
    def _register_user(self):
        self.user = UserFactory.create()
        self.user.set_password("defaultpassword")
        self.user.save()

    @pytest.fixture(autouse=True)
    def initialize(self):
        self._register_user()

        self.login_url = "http://127.0.0.1:8000/user/login/"
        self.login_request = {
            "username": self.user.username,
            "password": "defaultpassword",
        }

    def test_login_user_success(self, client):
        response = client.post(self.login_url, self.login_request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]
        assert response.data["refresh"]

    def test_login_user_wrong_password(self, client):
        bad_credentials = self.login_request
        bad_credentials["password"] = "wrong pass"
        response = client.post(self.login_url, bad_credentials)
        expected_response = {
            "detail": ErrorDetail(
                string="No active account found with the given credentials",
                code="no_active_account",
            )
        }

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == expected_response

    def test_login_user_wrong_username(self, client):
        bad_credentials = self.login_request
        bad_credentials["username"] = "non-existing user"
        response = client.post(self.login_url, bad_credentials)
        expected_response = {
            "detail": ErrorDetail(
                string="No active account found with the given credentials",
                code="no_active_account",
            )
        }

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data == expected_response

    def test_login_user_without_username(self, client):
        bad_credentials = self.login_request
        bad_credentials.pop("username")
        response = client.post(self.login_url, bad_credentials)
        expected_response = [
            ErrorDetail(string="This field is required.", code="required")
        ]

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["username"] == expected_response

    def test_login_user_without_password(self, client):
        bad_credentials = self.login_request
        bad_credentials.pop("password")
        response = client.post(self.login_url, bad_credentials)
        expected_response = [
            ErrorDetail(string="This field is required.", code="required")
        ]

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["password"] == expected_response

    def test_login_user_empty_username(self, client):
        bad_credentials = self.login_request
        bad_credentials["username"] = ""
        response = client.post(self.login_url, bad_credentials)
        expected_response = [
            ErrorDetail(string="This field may not be blank.", code="blank")
        ]

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["username"] == expected_response

    def test_login_user_empty_password(self, client):
        bad_credentials = self.login_request
        bad_credentials["password"] = ""
        response = client.post(self.login_url, bad_credentials)
        expected_response = [
            ErrorDetail(string="This field may not be blank.", code="blank")
        ]

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["password"] == expected_response


@pytest.mark.django_db
class TestLoginAdmin:
    def _register_admin(self):
        self.admin = UserFactory.create(is_superuser=True)
        self.admin.set_password("defaultpassword")
        self.admin.save()

    @pytest.fixture(autouse=True)
    def initialize(self):
        self._register_admin()

        self.login_url = "http://127.0.0.1:8000/user/login/"
        self.login_request = {
            "username": self.admin.username,
            "password": "defaultpassword",
        }

    def test_admin_login_success(self, client):
        response = client.post(self.login_url, self.login_request)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["access"]
        assert response.data["refresh"]
