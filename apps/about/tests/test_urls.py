from django.test import Client, TestCase
from django.urls import reverse

from apps.users.models import User


class AboutURLTest(TestCase):
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
            reverse('author'): 200,
            reverse('tech'): 200,
            reverse('foodgram'): 200,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = AboutURLTest.guest_client.get(name)
                self.assertEqual(response.status_code, status_code)

    def test_url_exists_for_authorized_users(self):
        """
        Test pages existing for authorized user.
        """
        pages_status_code = {
            reverse('author'): 200,
            reverse('tech'): 200,
            reverse('foodgram'): 200,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = AboutURLTest.authorized_client.get(name)
                self.assertEqual(response.status_code, status_code)

    def test_url_uses_correct_template(self):
        """
        Test URLs use correct templates.
        """
        templates_url_names = {
            reverse('author'): 'about/author.html',
            reverse('tech'): 'about/tech.html',
            reverse('foodgram'): 'about/foodgram.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = AboutURLTest.authorized_client.get(reverse_name)
                self.assertTemplateUsed(
                    response=response,
                    template_name=template,
                )
