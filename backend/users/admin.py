from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    """Модель юзера в админке"""
    list_display = ('is_active', 'username',
                    'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'first_name', 'email')


class FollowAdmin(admin.ModelAdmin):
    """Модель подписки в админке"""
    list_display = ('user', 'author')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
