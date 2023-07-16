from django.contrib import admin

from .models import Cart, Ingredient, Favorite, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Модель рецептов в админке"""
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    """Модель ингридиента в админке"""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Cart)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
