from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, HiddenField

from apps.recipes.models import Favorite, Follow, Ingredient, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for ingredients.
    """
    class Meta:
        fields = "__all__"
        model = Ingredient


class FavoriteSerializer(CurrentUserDefault, serializers.ModelSerializer):
    """
    Serializer for favorite recipes.
    """
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        fields = "__all__"
        model = Favorite


class PurchaseSerializer(CurrentUserDefault, serializers.ModelSerializer):
    """
    Serializer for purchase.
    """
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        fields = "__all__"
        model = Purchase


class FollowSerializer(CurrentUserDefault, serializers.ModelSerializer):
    """
    Serializer for following authors.
    """
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        fields = "__all__"
        model = Follow
