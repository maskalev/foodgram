from django.test import Client, TestCase
from django.urls import reverse

from apps.recipes.models import Purchase, Recipe
from apps.users.models import User


class RecipeFormTest(TestCase):
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
        cls.recipe = Recipe.objects.get(id=1)
        cls.purchase = Purchase.objects.get(id=1)

    def test_create_recipe_in_db(self):
        """
        New recipe is add to database.
        """
        self.assertEqual(Recipe.objects.count(), 8)
        Recipe.objects.create(
            title='recipe-title',
            description='recipe-description',
            cooking_time=10,
            slug='recipe-slug',
            author=RecipeFormTest.author
        )
        self.assertEqual(Recipe.objects.count(), 9)

    def test_delete_recipe_from_db(self):
        """
        Delete recipe from database.
        """
        self.assertEqual(Recipe.objects.count(), 8)
        response = RecipeFormTest.recipe_author.get(
            reverse('delete_recipe',
                    kwargs={
                        'username': RecipeFormTest.author.username,
                        'slug': RecipeFormTest.recipe.slug,
                    }))
        self.assertEqual(Recipe.objects.count(), 7)
