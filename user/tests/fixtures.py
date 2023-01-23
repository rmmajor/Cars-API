import pytest


@pytest.fixture
def registered_admin():
    pass


@pytest.fixture
def registered_user():
    pass


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



