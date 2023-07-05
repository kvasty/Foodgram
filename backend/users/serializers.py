from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериалайзер для кастомного юзера"""
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        """Проверка подписки"""
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.objects.filter(user=user, author=obj).exists()
        )

    def create(self, validated_data):
        """Создание пользователя"""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FollowSerializer(UserSerializer):
    """Подписки пользователя"""
    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count')

    def get_is_subscribed(self, obj):
        """Проверка подписки"""
        return User.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes_count(self, obj):
        """Кол-во рецептов юзера"""
        return obj.recipes.count()
