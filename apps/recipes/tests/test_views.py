from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from apps.recipes.models import Purchase, Recipe
from apps.users.models import User


class RecipeViewTest(TestCase):
    fixtures = ['recipes.json', 'users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
        cls.purchase = Purchase.objects.get(id=1)

    def test_index_page_show_correct_context(self):
        """
        Index page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context['recipe_list']), 6)
        self.assertEqual(response.context['recipe_list'][0],
                         RecipeViewTest.recipe)

    def test_authorlist_page_show_correct_context(self):
        """
        Authorlist page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(
            reverse('authorlist',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                    }))
        recipe_context = {
            len(response.context['recipe_list']): 6,
            response.context['recipe']: RecipeViewTest.recipe,
            response.context['author']: RecipeViewTest.author,
        }
        for test_value, expected_value in recipe_context.items():
            with self.subTest(expected_value=expected_value):
                self.assertEqual(test_value, expected_value)
        self.assertEqual(response.context['recipe_list'][0],
                         RecipeViewTest.recipe)

    def test_recipe_page_show_correct_context(self):
        """
        Recipe page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(
            reverse('recipe',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                        'slug': RecipeViewTest.recipe.slug,
                    }))
        recipe_context = {
            response.context['recipe']: RecipeViewTest.recipe,
            response.context['author']: RecipeViewTest.author,
        }
        for test_value, expected_value in recipe_context.items():
            with self.subTest(expected_value=expected_value):
                self.assertEqual(test_value, expected_value)

    def test_add_recipe_show_correct_context(self):
        """
        Add_recipe page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(reverse('add_recipe'))
        new_context = {
            'title': forms.fields.CharField,
            'description': forms.fields.CharField,
            'tags': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
            'cooking_time': forms.fields.IntegerField,
            'slug': forms.fields.SlugField,
            }
        for value, expected in new_context.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(obj=form_field, cls=expected)

    def test_edit_recipe_page_show_correct_context(self):
        """
        Edit recipe page show the correct context.
        """
        response = RecipeViewTest.recipe_author.get(
            reverse('edit_recipe',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                        'slug': RecipeViewTest.recipe.slug,
                    }))
        edit_context = {
            'title': forms.fields.CharField,
            'description': forms.fields.CharField,
            'tags': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
            'cooking_time': forms.fields.IntegerField,
            'slug': forms.fields.SlugField,
        }
        for value, expected in edit_context.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(obj=form_field, cls=expected)

    def test_favorites_page_show_correct_context(self):
        """
        Favorites page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(reverse('favorites'))
        self.assertEqual(len(response.context['recipe_list']), 1)
        self.assertEqual(response.context['recipe_list'][0],
                         RecipeViewTest.recipe)

    def test_subscriptions_page_show_correct_context(self):
        """
        Subscriptions page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(reverse('favorites'))
        self.assertEqual(len(response.context['recipe_list']), 1)
        self.assertEqual(response.context['recipe_list'][0],
                         RecipeViewTest.recipe)

    def test_purchases_page_show_correct_context(self):
        """
        Purchases page shows the correct context.
        """
        response = RecipeViewTest.authorized_client.get(reverse('purchases'))
        self.assertEqual(len(response.context['purchase_list']), 1)
        self.assertEqual(response.context['purchase_list'][0],
                         RecipeViewTest.purchase)

    def test_index_paginator_shows_correct_number_of_objects(self):
        """
        Paginator shows the correct number of objects on index page.
        """
        pages = {
            reverse('index'): 6,
            (reverse('index')+'?page=2'): 2,
        }
        for page, obj_count in pages.items():
            with self.subTest(page=page):
                response = RecipeViewTest.authorized_client.get(page)
                self.assertEqual(len(response.context['recipe_list']),
                                 obj_count)

    def test_authorlist_paginator_shows_correct_number_of_objects(self):
        """
        Paginator shows the correct number of objects on authorlist page.
        """
        pages = {
            reverse('authorlist',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                    }): 6,
            reverse('authorlist',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                     })+'?page=2': 1,
        }
        for page, obj_count in pages.items():
            with self.subTest(page=page):
                response = RecipeViewTest.authorized_client.get(page)
                self.assertEqual(len(response.context['recipe_list']),
                                 obj_count)

    def test_admin_delete_recipe(self):
        """
        Admin can delete a recipe.
        """
        self.assertEqual(Recipe.objects.count(), 8)
        RecipeViewTest.superuser.post(
            reverse('delete_recipe',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                        'slug': RecipeViewTest.recipe.slug,
                    }))
        self.assertEqual(Recipe.objects.count(), 7)

    def test_not_author_cannot_delete_recipe(self):
        """
        Not author cannot delete a recipe.
        """
        self.assertEqual(Recipe.objects.count(), 8)
        RecipeViewTest.authorized_client.post(
            reverse('delete_recipe',
                    kwargs={
                        'username': RecipeViewTest.author.username,
                        'slug': RecipeViewTest.recipe.slug,
                    }))
        self.assertEqual(Recipe.objects.count(), 8)

    def test_follow_author(self):
        """
        User who follows nobody don't see authors in Favorite.
        """
        response = RecipeViewTest.recipe_author.get(reverse('favorites'))
        self.assertEqual(len(response.context['recipe_list']), 0)
