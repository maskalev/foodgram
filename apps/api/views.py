from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers import (FavoriteSerializer, FollowSerializer,
                                  IngredientSerializer, PurchaseSerializer)
from apps.recipes.models import Favorite, Follow, Ingredient, Purchase


class CreateDestroyView(viewsets.ModelViewSet):
    """
    Create and destroy viewset.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        """
        Get object for current user.
        """
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {
            self.lookup_field: self.kwargs[self.lookup_field],
            'user': self.request.user,
        }

        object = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, object)
        return object

    def destroy(self, request, *args, **kwargs):
        """
        Delete the current instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={}, status=status.HTTP_200_OK)


class FavoritesView(CreateDestroyView):
    """
    Favorite recipes view.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe'


class PurchaseView(CreateDestroyView):
    """
    Purchase view.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = 'recipe'


class FollowView(CreateDestroyView):
    """
    Following authors view.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'author'


class IngredientsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Ingredients view.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)
