"""Projects filters."""
from django import template

from apps.recipes.models import Favorite, Follow, Purchase

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Encode URL with context.
    """
    query = context['request'].GET.copy()
    if query.get('page') is not None:
        query.pop('page')
    query.update(kwargs)
    return query.urlencode()


@register.filter
def shopcounter(user):
    """
    Recipes number in purchase list.
    """
    return user.purchases.count()


@register.filter
def isfollowing(author, user):
    """
    Return True if author is followed by user.
    """
    return Follow.objects.filter(author=author, user=user).exists()


@register.filter
def ispurchased(recipe, user):
    """
    Return True if recipe is in users's purchase list.
    """
    return Purchase.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def isfavorite(recipe, user):
    """
    Return True if recipe is in users's favorites.
    """
    return Favorite.objects.filter(recipe=recipe, user=user).exists()


@register.filter
def intmap(value):
    """
    Map list of ints.
    """
    return list(map(int, value))


@register.filter
def remainsrecipesnumber(number):
    """
    Return correct phrase.
    """
    remains = number % 10
    still_numbers = number - 3
    if 7 < number < 24:
        return f'Ещё {still_numbers} рецептов...'
    elif remains == 4:
        return f'Ещё {still_numbers} рецепт...'
    elif 4 < remains < 8:
        return f'Ещё {still_numbers} рецепта...'
    else:
        return f'Ещё {still_numbers} рецептов...'
