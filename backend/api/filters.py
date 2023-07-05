from django.contrib.auth import get_user_model
from django_filters.rest_framework import (
    AllValuesMultipleFilter,
    BooleanFilter,
    FilterSet,
    ModelChoiceFilter
)
from rest_framework.filters import SearchFilter

from api.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(SearchFilter):
    search_param = 'title'

    class Meta:
        model = Ingredient
        fields = ('title',)


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    is_favorited = BooleanFilter(
        method='get_is_favorited',
    )
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart',
    )
    author = ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favourites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
