from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.paginators import LimitPagePagination
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    Cart,
    IngredientToRecipe,
)
from .permissions import (
    IsOwnerOrReadOnly,
    IsAdminOrReadOnly,
)
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeShortSerializer,
    CreateRecipeSerializer
)
from .filters import (
    IngredientFilter,
    RecipeFilter
)


class TagsViewSet(ReadOnlyModelViewSet):
    """Обрабатывает тэги"""
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Обрабатывает ингридиенты"""
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^title',)


class RecipeViewSet(ModelViewSet):
    """Обрабатывает рецепты"""
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitPagePagination
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавить/удалить рецепт из избранного"""
        if request.method == 'POST':
            return self.add_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Добавить/удалить рецепт из списка покупок"""
        if request.method == 'POST':
            return self.add_obj(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Cart, request.user, pk)
        return None

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Рецепт уже добавлен'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        object = model.objects.filter(user=user, recipe__id=pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Загрузить список покупок"""
        user = self.request.user
        if not user.cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        filename = f"{user.username}_shopping_list.txt"
        ingredients = IngredientToRecipe.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__title', 'ingredient__units',
            'quantity')
        shopping_cart_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
        )
        shopping_cart_list += '\n'.join([
            f'- {ingredient["ingredient__title"]} '
            f'({ingredient["ingredient__units"]})'
            f' - {ingredient["quantity"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(
            shopping_cart_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
