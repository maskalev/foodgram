from django.test import Client, TestCase
from django.urls import reverse

from apps.recipes.models import Recipe
from apps.users.models import User


class RecipeURLTest(TestCase):
    fixtures = ['recipes.json', 'users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.get(id=3)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.author = User.objects.get(id=2)
        cls.recipe_author = Client()
        cls.recipe_author.force_login(cls.author)
        cls.admin = User.objects.get(id=1)
        cls.superuser = Client()
        cls.superuser.force_login(cls.admin)
        cls.recipe = Recipe.objects.get(id=1)

    def test_url_exists_for_anonymous(self):
        """
        Test pages existing for anonymous user.
        """
        pages_status_code = {
            reverse('index'):
                200,
            reverse('authorlist', kwargs={
                'username': RecipeURLTest.author.username}): 200,
            reverse('recipe', kwargs={
                'username': RecipeURLTest.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 200,
            reverse('subscriptions'): 302,
            reverse('favorites'): 302,
            reverse('purchases'): 302,
            reverse('purchase_list_pdf'): 302,
            reverse('add_recipe'): 302,
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 302,
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 302,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = RecipeURLTest.guest_client.get(name)
                assert response.status_code == status_code

    def test_url_exists_for_authorized_users(self):
        """
        Test pages existing for authorized user.
        """
        pages_status_code = {
            reverse('index'): 200,
            reverse('authorlist', kwargs={
                'username': RecipeURLTest.author.username}): 200,
            reverse('recipe', kwargs={
                'username': RecipeURLTest.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 200,
            reverse('subscriptions'): 200,
            reverse('favorites'): 200,
            reverse('purchases'): 200,
            reverse('purchase_list_pdf'): 200,
            reverse('add_recipe'): 200,
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 302,
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 302,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = RecipeURLTest.authorized_client.get(name)
                assert response.status_code == status_code

    def test_url_exists_for_recipe_author(self):
        """
        Test pages existing for recipe author.
        """
        pages_status_code = {
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 200,
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 302,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = RecipeURLTest.recipe_author.get(name)
                assert response.status_code == status_code

    def test_url_exists_for_admin(self):
        """
        Test pages existing for admin.
        """
        pages_status_code = {
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 200,
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 302,
        }
        for name, status_code in pages_status_code.items():
            with self.subTest(name=name):
                response = RecipeURLTest.superuser.get(name)
                assert response.status_code == status_code

    def test_url_redirect_anonymous(self):
        """
        Test redirect anonymous user to the correct page
        """
        redirect_pages = {
            reverse('subscriptions'): (reverse('login') + '?next='
                                       + reverse('subscriptions')),
            reverse('favorites'): (reverse('login') + '?next='
                                   + reverse('favorites')),
            reverse('purchases'): (reverse('login') + '?next='
                                   + reverse('purchases')),
            reverse('add_recipe'): (reverse('login') + '?next='
                                    + reverse('add_recipe')),
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): (reverse('login') + '?next='
                 + reverse('edit_recipe', kwargs={
                        'username': RecipeURLTest.recipe.author.username,
                        'slug': RecipeURLTest.recipe.slug
                    })),
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): (reverse('login') + '?next='
                 + reverse('delete_recipe', kwargs={
                        'username': RecipeURLTest.recipe.author.username,
                        'slug': RecipeURLTest.recipe.slug
                    })),
        }
        for donor, expected in redirect_pages.items():
            with self.subTest(donor=donor):
                response = RecipeURLTest.guest_client.get(donor, follow=True)
                self.assertRedirects(response=response, expected_url=expected)

    def test_url_redirect_authorized_user(self):
        """
        Test redirect authorized user to the correct page
        """
        redirect_pages = {
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): reverse('index'),
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): reverse('index'),
        }
        for donor, expected in redirect_pages.items():
            with self.subTest(donor=donor):
                response = RecipeURLTest.authorized_client.get(donor,
                                                               follow=True)
                self.assertRedirects(response=response, expected_url=expected)

    def test_url_redirect_recipe_author(self):
        """
        Test redirect recipe author to the correct page
        """
        redirect_pages = {
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): reverse('index'),
        }
        for donor, expected in redirect_pages.items():
            with self.subTest(donor=donor):
                response = RecipeURLTest.recipe_author.get(donor, follow=True)
                self.assertRedirects(response=response, expected_url=expected)

    def test_url_redirect_admin(self):
        """
        Test redirect admin to the correct page
        """
        redirect_pages = {
            reverse('delete_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): reverse('index'),
        }
        for donor, expected in redirect_pages.items():
            with self.subTest(donor=donor):
                response = RecipeURLTest.superuser.get(donor, follow=True)
                self.assertRedirects(response=response, expected_url=expected)

    def test_url_uses_correct_template(self):
        """
        Test URLs use correct templates.
        """
        templates_url_names = {
            reverse('index'): 'recipes/recipe_list.html',
            reverse('authorlist', kwargs={
                'username': RecipeURLTest.author.username
            }): 'recipes/recipe_list.html',
            reverse('recipe', kwargs={
                'username': RecipeURLTest.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 'recipes/recipe_detail.html',
            reverse('subscriptions'): 'recipes/follow_list.html',
            reverse('favorites'): 'recipes/recipe_list.html',
            reverse('purchases'): 'recipes/purchase_list.html',
            reverse('add_recipe'): 'recipes/recipe_form.html',
            reverse('edit_recipe', kwargs={
                'username': RecipeURLTest.recipe.author.username,
                'slug': RecipeURLTest.recipe.slug
            }): 'recipes/recipe_form.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = RecipeURLTest.recipe_author.get(reverse_name)
                self.assertTemplateUsed(
                    response=response,
                    template_name=template,
                )
