from django.test import TestCase
from rest_framework import test, status
from django.urls import reverse
from .views import BrandViewSet


# Tests for Brand endpoints.
class TestBrandInstanceCRUD(test.APITestCase):

    def test_testing(self):
        response = self.client.get(reverse('brand-list', current_app='brand'))
        print(response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

