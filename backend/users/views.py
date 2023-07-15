from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginators import LimitPagePagination
from .models import Follow
from api.serializers import FollowSerializer, CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Обрабатывает кастомного юзера"""
    queryset = User.objects.all()
    pagination_class = LimitPagePagination
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Подписка/отписка юзера"""
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user == author:
                return Response({
                    'errors': 'Подписка на самого себя не разрешена'
                }, status=status.HTTP_400_BAD_REQUEST)
            if user.follower.filter(author=author).exists():
                return Response({
                    'errors': 'Подписка уже состоялась'
                }, status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(author,
                                          data=request.data,
                                          context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            follow = get_object_or_404(Follow, user=user, author=author)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Подписки пользователя"""
        user = self.request.user
        queryset = User.objects.filter(follower__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
