from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from foodgram.settings import MAX_LENGTH

User = get_user_model()


class Ingredient(models.Model):
    """Ингридиент для рецепта"""
    name = models.CharField(
        'название',
        max_length=MAX_LENGTH,
        db_index=True
    )
    measurement_unit = models.CharField(
        'единицы измерения',
        max_length=MAX_LENGTH)

    class Meta:
        ordering = ['name']
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique_ingredient')
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тэг для рецепта"""
    name = models.CharField('название', unique=True, max_length=MAX_LENGTH)
    color = models.CharField(
        'цвет',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        'ссылка',
        max_length=MAX_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField('название', max_length=MAX_LENGTH)
    image = models.ImageField(
        'картинка',
        upload_to='recipes/',
        blank=True,
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.name


class IngredientToRecipe(models.Model):
    """Инридиенты для рецепта"""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[MinValueValidator(1, message='Минимальное количество 1')]
    )

    class Meta:
        verbose_name = 'связь рецепта и ингредиента'
        verbose_name_plural = 'связи рецептов и ингредиентов'

    def __str__(self):
        return (f'Связь ингредиента {self.ingredient.name}',
                f'и рецепта: {self.recipe.name}')


class Favorite(models.Model):
    """Модель избранного рецепта"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe for user')
        ]


class Cart(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'корзина'
        verbose_name_plural = 'в корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart user')
        ]
