from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from recipes.models import Cart, Ingredient, Favorite, Recipe, Tag
from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    """Модель юзера в админке"""
    list_display = ('is_active', 'username',
                    'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'first_name', 'email')


class FollowAdmin(admin.ModelAdmin):
    """Модель подписки в админке"""
    list_display = ('user', 'author')


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
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
