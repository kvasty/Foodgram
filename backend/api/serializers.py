from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from drf_extra_fields.fields import Base64ImageField

from users.serializers import (
    CustomUserSerializer
)
from recipes.models import (
    Ingredient,
    IngredientToRecipe,
    Recipe,
    Tag,
)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Выводим все поля тэгов"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Выводим все поля ингридиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeShortSerializer(serializers.ModelSerializer):
    """Краткая информация о рецепте"""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = 'id', 'title', 'image', 'cooking_time'
        read_only_fields = ('__all__',)


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """ Добавление ингредиента в рецепт"""

    id = serializers.IntegerField()

    class Meta:
        model = IngredientToRecipe
        fields = ['id', 'quantity']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Ингридиенты запрашиваемого рецепта"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    title = serializers.ReadOnlyField(source='ingredient.title')
    units = serializers.ReadOnlyField(source='ingredient.units')

    class Meta:
        model = IngredientToRecipe
        fields = ('id', 'title', 'units', 'quantity', )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер вывода для рецепта"""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'title',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        """Ингридиенты для рецепта"""
        ingredients = IngredientToRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        """Находится ли рецепт в избранных"""
        user = self.context.get('request').user
        return (False if user.is_anonymous
                else user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        """Находится ли рецепт в списке покупок"""
        user = self.context.get('request').user
        return (False if user.is_anonymous
                else user.carts.filter(recipe=obj).exists())


class CreateRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор создания/обновления рецепта"""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = AddIngredientRecipeSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'title',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        """Корректность заполнения/редактирования рецепта"""
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        if not ingredients or not tags:
            raise ValidationError('Некорректные данные')
        data.update(
            {
                'tags': tags,
                'ingredients': ingredients,
                'author': self.context.get('request').user
            }
        )
        return data

    def create(self, validated_data):
        """Создание рецепта"""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        image = validated_data.pop('image')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients_to_recipe(ingredients, recipe)
        return recipe

    def create_ingredients_to_recipe(self, ingredients, recipe):
        """Связь ингридиентов и рецепта"""
        for ingredient in ingredients:
            IngredientToRecipe.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                quantity=ingredient.get('quantity'),
            )

    def update(self, instance, validated_data):
        """Обновление рецепта"""
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        instance = super().update(instance, validated_data)
        self.create_ingredients_to_recipe(recipe=instance,
                                          ingredients=ingredients)
        instance.save()
        return instance


class FollowSerializer(CustomUserSerializer):
    """Подписки пользователя"""
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + (
            'recipes_count', 'recipes'
        )
        read_only_fields = ('email', 'username')

    def get_recipes_count(self, obj):
        """Кол-во рецептов юзера"""
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeShortSerializer(recipes, many=True, read_only=True)
        return serializer.data
