from django.contrib import admin

from .models import Cart, Ingredient, Favorite, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    """Модель рецептов в админке"""
    list_display = ('title', 'author')
    list_filter = ('author', 'title', 'tags')

    def count_favorites(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    """Модель ингридиента в админке"""
    list_display = ('title', 'units')
    list_filter = ('title',)


admin.site.register(Cart)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
