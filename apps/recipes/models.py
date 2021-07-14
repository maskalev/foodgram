from django.core.validators import MinValueValidator
from django.db import models

from apps.users.models import User


class Ingredient(models.Model):
    """
    Ingredient model.
    """
    title = models.CharField(
        max_length=255,
        verbose_name='Ingredient title',
        unique=True
    )
    unit = models.CharField(
        max_length=30,
        verbose_name='Unit of measurement'
    )

    def __str__(self):
        return f'{self.title} ({self.unit})'

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'


class Tag(models.Model):
    """
    Tag model (breakfast, lunch and dinner).
    """
    title = models.CharField(
        max_length=20,
        verbose_name='Tag title'
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Tag slug',
    )
    color = models.CharField(
        max_length=20,
        default='green',
        verbose_name='Tag color'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Recipe(models.Model):
    """
    Recipe model.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Title',
    )
    description = models.TextField(
        verbose_name='Description',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Tag',
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Image',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Cooking time, min',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredients',
        related_name='recipes',
        verbose_name='Ingredients',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date',
    )
    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
        verbose_name='Recipe slug',
    )

    def __str__(self):
        return f'{self.title}, {self.author}, {self.pub_date}'

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'


class RecipeIngredients(models.Model):
    """
    Link between recipes and ingredients.
    """
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Recipe',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ingredient',
    )
    quantity = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Quantity',
    )

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}, {self.quantity}'

    class Meta:
        verbose_name_plural = 'RecipesIngredients'
        verbose_name = 'RecipeIngredients'
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'ingredient'),
                                    name='unique_link'),
        ]


class Favorite(models.Model):
    """
    Link between users and favorite recipes.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Recipe',
    )

    def __str__(self):
        return f'{self.user}, {self.recipe}'

    class Meta:
        verbose_name_plural = 'Favorite'
        verbose_name = 'Favorites'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_favorites_link'),
        ]


class Purchase(models.Model):
    """
    Link between user and his shopping cart.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name='Recipe',
    )

    def __str__(self):
        return f'{self.user}, {self.recipe}'

    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_purchase_link'),
        ]


class Follow(models.Model):
    """
    Link between follower and following.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Author',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower',
    )

    def __str__(self):
        return f'{self.author}, {self.user}'

    class Meta:
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'
        constraints = [
            models.UniqueConstraint(fields=('author', 'user'),
                                    name='unique_follow_link'),
        ]
