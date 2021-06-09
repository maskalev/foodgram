from django.http import JsonResponse
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.api.serializers import (FavoriteSerializer, PurchaseSerializer,
                                  FollowSerializer, IngredientSerializer)
from apps.recipes.models import Favorite, Purchase, Follow, Ingredient


class CreateDestroyView(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
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


@api_view(['GET'])
@permission_classes([AllowAny])
def api_get_ingredients(request):
    query = request.GET.get('query')
    if query is not None:
        ingredients = Ingredient.objects.filter(name__startswith=query)
        serializer = IngredientSerializer(ingredients, many=True)
        return JsonResponse(serializer.data, safe=False)
    return Response({'error': 'query is empty'})
