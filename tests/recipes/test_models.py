from django.test import TestCase

from apps.recipes.models import (Favorite, Follow, Ingredient, Purchase,
                                 Recipe, RecipeIngredients, Tag)


class RecipeModelTest(TestCase):
    fixtures = ["recipes.json", "users.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.recipe = Recipe.objects.get(id=1)
        cls.ingredient = Ingredient.objects.get(id=1)
        cls.tag = Tag.objects.get(id=1)
        cls.recipeingredients = RecipeIngredients.objects.get(id=1)
        cls.favorite = Favorite.objects.get(id=1)
        cls.purchase = Purchase.objects.get(id=1)
        cls.follow = Follow.objects.get(id=1)

    def test_ingredient_verbose_name(self):
        """
        Verbose names in Ingredient model are expected.
        """
        ingredient = RecipeModelTest.ingredient
        field_verbose = {
            "name": "Ingredient title",
            "unit": "Unit of measurement",
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert (ingredient._meta.get_field(value).verbose_name ==
                        expected)

    def test_tag_verbose_name(self):
        """
        Verbose names in Tag model are expected.
        """
        tag = RecipeModelTest.tag
        field_verbose = {
            "title": "Tag title",
            "slug": "Tag slug",
            "color": "Tag color"
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert tag._meta.get_field(value).verbose_name == expected

    def test_recipe_verbose_name(self):
        """
        Verbose names in Recipe model are expected.
        """
        recipe = RecipeModelTest.recipe
        field_verbose = {
            "title": "Title",
            "description": "Description",
            "author": "Author",
            "tags": "Tag",
            "image": "Image",
            "cooking_time": "Cooking time, min",
            "ingredients": "Ingredients",
            "pub_date": "Publication date",
            "slug": "Recipe slug"
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert recipe._meta.get_field(value).verbose_name == expected

    def test_recipeingredients_verbose_name(self):
        """
        Verbose names in RecipeIngredients model are expected.
        """
        recipeingredients = RecipeModelTest.recipeingredients
        field_verbose = {
            "recipe": "Recipe",
            "ingredient": "Ingredient",
            "quantity": "Quantity"
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert (recipeingredients._meta.get_field(value).verbose_name
                        == expected)

    def test_favorite_verbose_name(self):
        """
        Verbose names in Favorite model are expected.
        """
        favorite = RecipeModelTest.favorite
        field_verbose = {
            "user": "User",
            "recipe": "Recipe",
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert favorite._meta.get_field(value).verbose_name == expected

    def test_purchase_verbose_name(self):
        """
        Verbose names in Purchase model are expected.
        """
        purchase = RecipeModelTest.purchase
        field_verbose = {
            "user": "User",
            "recipe": "Recipe",
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert purchase._meta.get_field(value).verbose_name == expected

    def test_follow_verbose_name(self):
        """
        Verbose names in Follow model are expected.
        """
        follow = RecipeModelTest.follow
        field_verbose = {
            "author": "Author",
            "user": "Follower",
        }
        for value, expected in field_verbose.items():
            with self.subTest(value=value):
                assert follow._meta.get_field(value).verbose_name == expected

    def test_ingredient_name(self):
        """
        Name of Ingredient object are expected.
        """
        ingredient = RecipeModelTest.ingredient
        expected_object_name = f"{ingredient.name} ({ingredient.unit})"
        assert expected_object_name == str(ingredient)

    def test_tag_name(self):
        """
        Name of Tag object are expected.
        """
        tag = RecipeModelTest.tag
        expected_object_name = f"{tag.title}"
        assert expected_object_name == str(tag)

    def test_recipe_name(self):
        """
        Name of Recipe object are expected.
        """
        recipe = RecipeModelTest.recipe
        expected_object_name = f"{recipe.title} by {recipe.author}"
        assert expected_object_name == str(recipe)

    def test_recipeingredients_name(self):
        """
        Name of RecipeIngredients object are expected.
        """
        recipeingredients = RecipeModelTest.recipeingredients
        expected_object_name = (f"{recipeingredients.recipe}, "
                                f"{recipeingredients.ingredient}, "
                                f"{recipeingredients.quantity}")
        assert expected_object_name == str(recipeingredients)

    def test_favorite_name(self):
        """
        Name of Favorite object are expected.
        """
        favorite = RecipeModelTest.favorite
        expected_object_name = f"{favorite.user} marked {favorite.recipe}"
        assert expected_object_name == str(favorite)

    def test_purchase_name(self):
        """
        Name of Purchase object are expected.
        """
        purchase = RecipeModelTest.purchase
        expected_object_name = (f"{purchase.user} add to purchase "
                                f"{purchase.recipe}")
        assert expected_object_name == str(purchase)

    def test_follow_name(self):
        """
        Name of Follow object are expected.
        """
        follow = RecipeModelTest.follow
        expected_object_name = f"{follow.user} follows {follow.author}"
        assert expected_object_name == str(follow)
