import pytest
from rest_framework import status
from rest_framework.exceptions import ErrorDetail


@pytest.fixture
def good_registration_credentials():
    return dict(
        username="testUserName",
        email="testUserName@mail.test",
        password="testUserName",
        confirmed_password="testUserName"
    )


@pytest.fixture
def registration_url():
    return 'http://127.0.0.1:8000/user/create/'


@pytest.fixture
def registered_user():
    pass


@pytest.fixture
def registered_admin():
    pass


# Create your tests here.
@pytest.mark.django_db  # <- will create a mock database for you to test
def test_register_user_success(client, good_registration_credentials, registration_url):

    response = client.post(registration_url, good_registration_credentials)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['access']
    assert response.data['refresh']


@pytest.mark.django_db
def test_register_user_passwords_mismatch(client, good_registration_credentials, registration_url):

    bad_registration_credentials = good_registration_credentials
    bad_registration_credentials['confirmed_password'] = 'mismatched pass'
    response = client.post(registration_url, bad_registration_credentials)
    expected_response = {'non_field_errors': [ErrorDetail(string='Entered passwords mismatched', code='invalid')]}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_response


@pytest.mark.django_db
def test_register_user_without_confirmed_password(client, good_registration_credentials, registration_url):
    bad_credentials = good_registration_credentials
    bad_credentials.pop('confirmed_password')
    response = client.post(registration_url, bad_credentials)
    expected_response = {"confirmed_password": [
        "This field is required."
    ]}

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_response


@pytest.mark.django_db
def test_register_user_without_bad_password(client, good_registration_credentials, registration_url):
    """
    Tests password mask (bad caracters, less than 8 caracters, more than 28, etc)
    """
    # todo: add Parametrization later

    bad_credentials = good_registration_credentials
    bad_credentials['password'] = "1"
    bad_credentials['confirmed_password'] = "1"
    response = client.post(registration_url, bad_credentials)

    print(response.status_code)


@pytest.mark.django_db
def test_register_user_bad_username(client, good_registration_credentials, registration_url):
    pass


@pytest.mark.django_db
def test_register_user_bad_email(client, good_registration_credentials, registration_url):
    pass
