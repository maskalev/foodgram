"""Projects filters."""
from django import template
from django.urls import Resolver404, resolve

from apps.recipes.models import Favorite, Follow, Purchase

register = template.Library()


@register.simple_tag
def active_page(request, view_name):
    """
    Mark active page.
    """
    if not request:
        return ''
    try:
        return 'nav__item_active' if resolve(
            request.path_info).url_name == view_name else ''
    except Resolver404:
        return ''


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
def as_p(text, css):
    """
    Return HTML markup for text.
    """
    return ''.join(list(map(lambda x: f'<p class="{css}">{x}</p>',
                            text.split('\n'))))


@register.filter
def intmap(value):
    """
    Map list of ints.
    """
    return list(map(int, value))


@register.filter
def addclass(field, css):
    """
    Return class for input fields.
    """
    return field.as_widget(attrs={'class': css})


@register.filter
def remainsrecipesnumber(numder):
    """
    Return correct end of the phrase.
    """
    remains = numder % 10 - 3
    if remains == 1:
        return f'Ещё {remains} рецепт...'
    elif remains < 5:
        return f'Ещё {remains} рецепта...'
    else:
        return f'Ещё {remains} рецептов...'
