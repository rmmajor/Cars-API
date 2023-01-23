import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

registration_credentials = dict(
        username="testUserName",
        email="testUserName@mail.test",
        password="testUserName",
        confirmed_password="testUserName"
    )

registration_url = 'http://127.0.0.1:8000/user/create/'


# Create your tests here.
@pytest.mark.django_db
def test_register_user_success(client):

    response = client.post(registration_url, registration_credentials)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_register_user_passwords_mismatch(client):

    bad_credentials = registration_credentials
    bad_credentials['confirmed_password'] = 'mismatched pass'
    response = client.post(registration_url, bad_credentials)
    expected_data = {'non_field_errors': [ErrorDetail(string='Entered passwords mismatched', code='invalid')]}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_data


@pytest.mark.django_db
def test_register_user_without_confirmed_password(client):
    bad_credentials = registration_credentials
    bad_credentials.pop('confirmed_password')
    response = client.post(registration_url, bad_credentials)
    # expected_data = {'non_field_errors': [ErrorDetail(string='Entered passwords mismatched', code='invalid')]}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # assert response.data == expected_data


