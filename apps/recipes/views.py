import urllib

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from apps.recipes.forms import RecipeForm, TagForm
from apps.recipes.models import Follow, Purchase, Recipe, Tag
from apps.recipes.utils import create_pdf
from apps.users.models import User
from foodgram.settings import PAGINATOR, LOGIN_URL
from foodgram.urls import handler404


class RecipeList(ListView):
    """
    ListView for recipes.
    """
    model = Recipe
    paginate_by = PAGINATOR
    template_name = 'recipes/recipe_list.html'

    def get_queryset(self):
        default_filter = Tag.objects.values_list('id')
        posted_filter = self.request.GET.getlist('tags', default_filter)
        queryset = Recipe.objects.filter(tags__in=posted_filter).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TagForm(self.request.GET or None)
        return context


class AuthorList(RecipeList):
    """
    List view for recipes by one author.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        author = get_object_or_404(User, username=self.kwargs['username'])
        return queryset.filter(author=author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(User, username=self.kwargs['username'])
        context['author'] = author
        if self.request.user.is_authenticated:
            following = Follow.objects.filter(author=author,
                                              user=self.request.user).exists()
        else:
            following = False
        context['following'] = following
        return context


class RecipeDetail(DetailView):
    """
    DetailView for recipe.
    """
    model = Recipe
    template_name = 'recipes/recipe_detail.html'


class FavoritesList(LoginRequiredMixin, RecipeList):
    """
    ListView for favorites page.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        all_favorites = self.request.user.favorites.all().values('recipe')
        return queryset.filter(id__in=all_favorites)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = True
        return context


class FollowList(LoginRequiredMixin, ListView):
    """
    ListView for following's page of the user.
    """
    model = Follow
    paginate_by = PAGINATOR
    template_name = 'recipes/follow_list.html'

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class PurchaseList(LoginRequiredMixin, ListView):
    """
    ListView for recipes in purchase list.
    """
    model = Purchase
    template_name = 'recipes/purchase_list.html'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    """
    Add or edit the recipe.
    """
    recipe = None
    user = get_object_or_404(User, username=request.user.username)
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe,
                                   author__username=username,
                                   slug=slug)
        if request.user != recipe.author and request.user.is_superuser is False:
            return redirect('index')
    recipe_form = RecipeForm(request.POST or None, request.FILES or None,
                             instance=recipe)
    if recipe_form.is_valid():
        recipe = recipe_form.save(user=request.user)
        return redirect(reverse('recipe', args=(recipe.author, recipe.slug)))
    return render(request, 'recipes/recipe_form.html',
                  {
                      'form': recipe_form,
                      'recipe': recipe,
                  })


@login_required
def delete_recipe(request, username, slug):
    """
    Delete the recipe.
    """
    recipe = get_object_or_404(Recipe,
                               author__username=username,
                               slug=slug)
    if request.user.is_superuser or request.user == recipe.author:
        recipe.delete()
    else:
        pass
    return redirect('index')


@login_required
def purchase_list_pdf(request):
    """
    Create PDF from purchase list.
    """
    ingredients = request.user.purchases.select_related(
        'recipe'
    ).order_by(
        'recipe__ingredients__title'
    ).values(
        'recipe__ingredients__title', 'recipe__ingredients__unit'
    ).annotate(quantity=Sum('recipe__recipeingredients__quantity')).all()
    return create_pdf(ingredients, 'purchase_list.pdf')


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        'misc/500.html',
        {'path': request.path},
        status=500
    )
