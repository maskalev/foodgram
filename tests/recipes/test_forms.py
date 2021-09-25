from django.test import Client, TestCase
from django.urls import reverse

from apps.recipes.models import Purchase, Recipe, RecipeIngredients, Ingredient
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
        cls.ingredient = Ingredient.objects.get(id=2)
        cls.recipe_ingredient = RecipeIngredients.objects.get(id=1)

    def test_create_recipe_in_db(self):
        """
        New recipe is add to database.
        """
        assert Recipe.objects.count() == 8
        Recipe.objects.create(
            title='recipe-title',
            description='recipe-description',
            cooking_time=10,
            slug='recipe-slug',
            author=RecipeFormTest.author
        )
        assert Recipe.objects.count() == 9

    def test_delete_recipe_from_db(self):
        """
        Delete recipe and recipe's ingredients from database.
        """
        assert Recipe.objects.count() == 8
        assert RecipeIngredients.objects.count() == 8
        RecipeFormTest.recipe_author.get(
            reverse('delete_recipe',
                    kwargs={
                        'username': RecipeFormTest.author.username,
                        'slug': RecipeFormTest.recipe.slug,
                    }))
        assert Recipe.objects.count() == 7
        assert RecipeIngredients.objects.count() == 7
