from django.core.validators import MinValueValidator
from django.db import models

from apps.users.models import User


class Ingredient(models.Model):
    """
    Ingredient model.
    """
    name = models.CharField(
        max_length=255,
        verbose_name="Ingredient title",
        unique=True
    )
    unit = models.CharField(
        max_length=30,
        verbose_name="Unit of measurement"
    )

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Tag(models.Model):
    """
    Tag model (breakfast, lunch and dinner).
    """
    title = models.CharField(
        max_length=20,
        verbose_name="Tag title",
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name="Tag slug",
    )
    color = models.CharField(
        max_length=20,
        default="green",
        verbose_name="Tag color"
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"{self.title}"


class Recipe(models.Model):
    """
    Recipe model.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
    )
    description = models.TextField(
        verbose_name="Description",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Author",
    )
    tags = models.ManyToManyField(
        "Tag",
        related_name="recipes",
        verbose_name="Tag",
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Image",
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name="Cooking time, min",
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredients",
        related_name="recipes",
        verbose_name="Ingredients",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Publication date",
    )
    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
        verbose_name="Recipe slug",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return f"{self.title} by {self.author}"


class RecipeIngredients(models.Model):
    """
    Link between recipes and ingredients.
    """
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        related_name="recipeingredients",
        verbose_name="Recipe",
    )
    ingredient = models.ForeignKey(
        "Ingredient",
        on_delete=models.CASCADE,
        related_name="recipeingredients",
        verbose_name="Ingredient",
    )
    quantity = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name="Quantity",
    )

    class Meta:
        verbose_name_plural = "RecipesIngredients"
        verbose_name = "RecipeIngredients"
        constraints = [
            models.UniqueConstraint(fields=("recipe", "ingredient"),
                                    name="unique_link"),
        ]

    def __str__(self):
        return f"{self.recipe}, {self.ingredient}, {self.quantity}"


class Favorite(models.Model):
    """
    Link between users and favorite recipes.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="User",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name="Recipe",
    )

    class Meta:
        verbose_name_plural = "Favorite"
        verbose_name = "Favorites"
        constraints = [
            models.UniqueConstraint(fields=("user", "recipe"),
                                    name="unique_favorites_link"),
        ]

    def __str__(self):
        return f"{self.user} marked {self.recipe}"


class Purchase(models.Model):
    """
    Link between user and his shopping cart.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="User",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Recipe",
    )

    class Meta:
        verbose_name = "Purchase"
        verbose_name_plural = "Purchases"
        constraints = [
            models.UniqueConstraint(fields=("user", "recipe"),
                                    name="unique_purchase_link"),
        ]

    def __str__(self):
        return f"{self.user} add to purchase {self.recipe}"


class Follow(models.Model):
    """
    Link between follower and following.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Author",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Follower",
    )

    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        constraints = [
            models.UniqueConstraint(fields=("author", "user"),
                                    name="unique_follow_link"),
        ]

    def __str__(self):
        return f"{self.user} follows {self.author}"
