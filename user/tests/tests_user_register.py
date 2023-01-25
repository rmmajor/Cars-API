import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from .factories import *
import factory


# Create your tests here.
@pytest.mark.django_db
class TestRegisterUser:

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.good_registration_credentials = dict(
            username="testUserName",
            email="testUserName@mail.test",
            password="testUserName",
            confirmed_password="testUserName"
        )

        self.registration_url = 'http://127.0.0.1:8000/user/create/'

    def test_register_user_success(self, client):

        response = client.post(self.registration_url, self.good_registration_credentials)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['access']
        assert response.data['refresh']

    def test_register_user_passwords_mismatch(self, client):

        bad_registration_credentials = self.good_registration_credentials
        bad_registration_credentials['confirmed_password'] = 'mismatched pass'
        response = client.post(self.registration_url, bad_registration_credentials)
        expected_response = {'non_field_errors': [ErrorDetail(string='Entered passwords mismatched', code='invalid')]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_response

    def test_register_user_without_confirmed_password(self, client):
        bad_credentials = self.good_registration_credentials
        bad_credentials.pop('confirmed_password')
        response = client.post(self.registration_url, bad_credentials)
        expected_response = {"confirmed_password": [
            "This field is required."
        ]}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == expected_response

    def test_register_user_without_bad_password(self, client):
        """
        Tests password mask (bad caracters, less than 8 caracters, more than 28, etc)
        """
        # todo: add Parametrization later

        bad_credentials = self.good_registration_credentials
        bad_credentials['password'] = "1"
        bad_credentials['confirmed_password'] = "1"
        response = client.post(self.registration_url, bad_credentials)

        print(response.status_code)

    def test_register_user_too_long_username(self, client):
        bad_credentials = self.good_registration_credentials
        long_username = "FvM4sgubtxXwelCTl1LHrb3lUrpGIpnBgDVQxnIfcK6EUyXYC" \
                        "b0etf6oNsUyMsdMYPomre8JILcbDQP6s8q4l7BVR8EFYXclbtI" \
                        "LfAVQGDPDsTZGcgafHynWWT4tuZBRcgy4vqymf67tb61Flzp5YG3"

        bad_credentials['username'] = long_username
        response = client.post(self.registration_url, bad_credentials)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'username': [ErrorDetail(string='Ensure this field has no more than 150 characters.',
                                                          code='max_length')]}

    def test_register_user_bad_email(self, client):
        bad_credentials = self.good_registration_credentials
        bad_email = "not email"

        bad_credentials['email'] = bad_email
        response = client.post(self.registration_url, bad_credentials)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'email': [ErrorDetail(string='Enter a valid email address.', code='invalid')]}
