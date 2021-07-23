from collections import OrderedDict

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
        cls.user = User.objects.get(id=3)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_response_data(self):
        """
        Response data is correct.
        """
        pages_data = {
            reverse('favorite-list'): OrderedDict([('id', 1), ('recipe', 1)]),
            reverse('purchase-list'): OrderedDict([('id', 1), ('recipe', 1)]),
            reverse('follow-list'): OrderedDict([('id', 1), ('author', 2)]),
            reverse('ingredient-list'): OrderedDict([
                ('id', 1),
                ('title', 'ingredient1'),
                ('unit', 'unit1')]),
        }
        for name, data in pages_data.items():
            with self.subTest(name=name):
                response = ApiURLTest.authorized_client.get(name)
                self.assertEqual(response.data[0], data)
