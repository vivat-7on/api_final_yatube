from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from posts.models import Comment, Post, Follow, Group, User
from .permissions import IsAuthorOrReadOnly
from .serializers import (PostSerializer,
                          GroupSerializer,
                          CommentSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Post.objects.all().select_related('author')
        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(
            post=post_id
        ).select_related('author')
        return queryset


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('following__username',)

    def perform_create(self, serializer):
        following_username = self.request.data.get('following')
        if not following_username:
            raise ValidationError({"following": ["Обязательное поле."]})

        try:
            following_user = User.objects.get(username=following_username)
        except User.DoesNotExist:
            raise ValidationError(
                {"following": ["Пользователь с указанным"
                               " 'following' не существует."]}
            )

        current_user = self.request.user

        if following_user == current_user:
            raise ValidationError(
                {"following": ["Нельзя подписаться на самого себя!"]}
            )

        if Follow.objects.filter(
                user=current_user,
                following=following_user
        ).exists():
            raise ValidationError(
                {"following": ["Вы уже подписаны на этого пользователя."]}
            )

        serializer.is_valid(raise_exception=True)
        serializer.save(user=current_user, following=following_user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(following__username__icontains=search)
        return queryset
