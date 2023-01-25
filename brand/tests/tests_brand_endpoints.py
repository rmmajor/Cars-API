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

    def test_get_brand_detail_success(self):
        brand_records = self._generate_brands(5)
        brand_id = 2
        url = reverse("brand-detail", args=(brand_id,))
        response = self.client.get(url)
        print(response.data)

        assert response.status_code == status.HTTP_200_OK

    def test_get_non_existing_instance_detail(self):
        brand_id = 1
        url = reverse("brand-detail", args=(brand_id,))
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_brands_empty_set(self):
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


@pytest.mark.django_db
class TestBrandPOSTbyAdmin:

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
        self.brand_list_url = 'http://127.0.0.1:8000/brands/'
        self.brand_to_post = factory.build(dict, FACTORY_CLASS=BrandFactory)
        self.brand_records = BrandFactory.create_batch(5)

    def test_post_success(self):
        response = self.client.post(self.brand_list_url, self.brand_to_post)
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_without_brand_name(self):
        bad_brand = self.brand_to_post
        bad_brand.pop('brand_name')
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_without_headquarters_country(self):
        bad_brand = self.brand_to_post
        bad_brand.pop('headquarters_country')
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_brand_name(self):
        bad_brand = self.brand_to_post
        bad_brand['brand_name'] = ''
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_post_with_empty_headquarters_country(self):
        bad_brand = self.brand_to_post
        bad_brand['headquarters_country'] = ''
        response = self.client.post(self.brand_list_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestBrandPUTbyAdmin:

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
        self.brand_detail_url = 'http://127.0.0.1:8000/brands/1/'
        self.brand_to_put = factory.build(dict, FACTORY_CLASS=BrandFactory)
        self.brand_records = BrandFactory.create_batch(5)

    def test_put_success(self):

        response = self.client.put(self.brand_detail_url, self.brand_to_put)
        assert response.status_code == status.HTTP_200_OK

    def test_put_without_brand_name(self):
        BrandFactory.create_batch(5)
        bad_brand = self.brand_to_put
        bad_brand.pop('brand_name')
        response = self.client.put(self.brand_detail_url, bad_brand)

        assert response.data == False
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_without_headquarters_country(self):
        bad_brand = self.brand_to_put
        bad_brand.pop('headquarters_country')
        response = self.client.put(self.brand_detail_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_with_empty_brand_name(self):
        bad_brand = self.brand_to_put
        bad_brand['brand_name'] = ''
        response = self.client.put(self.brand_detail_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_with_empty_headquarters_country(self):
        bad_brand = self.brand_to_put
        bad_brand['headquarters_country'] = ''
        response = self.client.put(self.brand_detail_url, bad_brand)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestBrandDELETEbyAdmin:

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
        self.brand_detail_url = 'http://127.0.0.1:8000/brands/1/'
        self.brand_records = BrandFactory.create_batch(5)

    def test_delete_brand_success(self):
        delete_response = self.client.delete(self.brand_detail_url)
        get_response = self.client.get(self.brand_detail_url)

        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_non_existing_brand(self):
        url = reverse("brand-detail", args=(404,))
        delete_response = self.client.delete(url)

        assert delete_response.status_code == status.HTTP_404_NOT_FOUND

