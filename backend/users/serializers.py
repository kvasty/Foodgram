from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField

from .models import Follow

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
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

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
