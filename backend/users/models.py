from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 100


class CustomUser(AbstractUser):
    """Кастомный юзер для фудграма"""
    username = models.CharField(
        unique=True,
        verbose_name='Логин',
        max_length=MAX_LENGTH
    )
    password = models.CharField(
        unique=True,
        verbose_name='Пароль',
        max_length=MAX_LENGTH
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        max_length=MAX_LENGTH
    )
    first_name = models.CharField(
        unique=True,
        verbose_name='Имя',
        max_length=MAX_LENGTH
    )
    last_name = models.CharField(
        unique=True,
        verbose_name='Фамилия',
        max_length=MAX_LENGTH
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Подписчик на автора рецепта"""
    user = models.ForeignKey(
        CustomUser,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow',
            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.author.username}'
