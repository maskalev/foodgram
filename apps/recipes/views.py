from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from apps.recipes.forms import TagForm, RecipeForm
from apps.recipes.models import Follow, Purchase, Recipe, Tag
from apps.recipes.utils import create_pdf
from apps.users.models import User
from foodgram.settings import PAGINATOR


class FollowList(LoginRequiredMixin, ListView):
    """
    ListView for following's page of the user.
    """
    model = Follow
    paginate_by = PAGINATOR

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class PurchaseList(LoginRequiredMixin, ListView):
    """
    ListView for recipes in purchase list.
    """
    model = Purchase

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


class RecipeList(ListView):
    """
    ListView for recipes.
    """
    model = Recipe
    paginate_by = PAGINATOR

    def get_queryset(self):
        default_filter = Tag.objects.values_list('id')
        posted_filter = self.request.GET.getlist('tags', default_filter)
        queryset = Recipe.objects.filter(tags__in=posted_filter).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TagForm(self.request.GET or None)
        return context


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
        following = (Follow.objects.filter(author=author,
                                           user=self.request.user).exists()
                     if self.request.user.is_authenticated
                     else False)
        context['following'] = following
        return context


class RecipeDetail(DetailView):
    """
    DetailView for recipe.
    """
    model = Recipe


@login_required
def add_or_edit_recipe(request, username=None, slug=None):
    """
    Add or edit the recipe.
    """
    recipe = None
    if username is not None and slug is not None:
        recipe = get_object_or_404(Recipe,
                                   author__username=username,
                                   slug=slug)
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
    return redirect('index')


@login_required
def confirm_delete(request, username, slug):
    """
    Confirmation to delete the recipe.
    """
    return render(request,
                  'recipes/recipe_delete.html',
                  {
                      'username': username,
                      'slug': slug,
                  })


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
