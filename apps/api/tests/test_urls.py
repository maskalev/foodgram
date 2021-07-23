from django.test import Client
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase

from apps.users.models import User


class ApiURLTest(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('v1/', include('apps.api.urls')),
    ]
    fixtures = ['recipes.json', 'users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.get(id=3)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_url_exists_for_anonymous(self):
        """
        Test pages existing for anonymous user.
        """
        pages_status_code = {
            reverse('favorite-list'): 403,
            reverse('purchase-list'): 403,
            reverse('follow-list'): 403,
            reverse('ingredient-list'): 200,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = ApiURLTest.guest_client.get(name)
                self.assertEqual(response.status_code, status_code)

    def test_url_exists_for_authorized_users(self):
        """
        Test pages existing for authorized user.
        """
        pages_status_code = {
            reverse('favorite-list'): 200,
            reverse('purchase-list'): 200,
            reverse('follow-list'): 200,
            reverse('ingredient-list'): 200,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = ApiURLTest.authorized_client.get(name)
                self.assertEqual(response.status_code, status_code)
