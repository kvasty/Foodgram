from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.settings import MAX_LENGTH


class CustomUser(AbstractUser):
    """Кастомный юзер для фудграма"""
    email = models.EmailField(
        unique=True,
        verbose_name='электронная почта',
        max_length=MAX_LENGTH
    )
    username = models.CharField(
        unique=True,
        verbose_name='логин',
        max_length=MAX_LENGTH
    )
    password = models.CharField(
        unique=True,
        verbose_name='пароль',
        max_length=MAX_LENGTH
    )
    first_name = models.CharField(
        unique=True,
        verbose_name='имя',
        max_length=MAX_LENGTH
    )
    last_name = models.CharField(
        unique=True,
        verbose_name='фамилия',
        max_length=MAX_LENGTH
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Подписчик на автора рецепта"""
    user = models.ForeignKey(
        CustomUser,
        verbose_name='подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='автор рецепта',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.author.username}'
