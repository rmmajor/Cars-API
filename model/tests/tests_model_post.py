import pytest
from rest_framework_simplejwt.tokens import RefreshToken
from ..factories import *
from user.tests.factories import *
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestModelPOSTbyAdmin:

    def _register_admin(self):
        self.admin = UserFactory.create(is_superuser=True)
        self.admin.set_password('password')
        self.admin.save()

        self.username = self.admin.username
        self.password = 'password'

        return RefreshToken.for_user(self.admin)

    def _login(self, refresh_token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token.access_token}')
        self.client.login(username=self.username, password=self.password)

    @pytest.fixture(autouse=True)
    def initialize(self):
        self.client = APIClient()
        admin_token = self._register_admin()
        self._login(admin_token)
        self.model_list_url = 'http://127.0.0.1:8000/models/'
        self.model_to_post = factory.build(dict, FACTORY_CLASS=ModelFactory)
        self.model_records = ModelFactory.create_batch(5)

    def test_post_success(self):
        response = self.client.post(self.model_list_url, self.model_to_post)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_without_model_name(self):
        bad_model = self.model_to_post
        bad_model.pop('model_name')
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_without_issue_year(self):
        bad_model = self.model_to_post
        bad_model.pop('issue_year')
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_without_body_style(self):
        bad_model = self.model_to_post
        bad_model.pop('body_style')
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_model_name(self):
        bad_model = self.model_to_post
        bad_model['model_name'] = ''
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_issue_year(self):
        bad_model = self.model_to_post
        bad_model['issue_year'] = ''
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_body_style(self):
        bad_model = self.model_to_post
        bad_model['body_style'] = ''
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_future_year(self):
        bad_model = self.model_to_post
        bad_model['issue_year'] = 2030
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_too_small_year(self):
        bad_model = self.model_to_post
        bad_model['issue_year'] = 988
        response = self.client.post(self.model_list_url, bad_model)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


