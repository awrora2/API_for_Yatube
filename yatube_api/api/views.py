from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Follow, Group, Post

from .permissions import IsUserOrReadOnlyPermission
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление недоступно чужого контента запрещено!')
        instance.delete()


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление недоступно чужого контента запрещено!')
        instance.delete()


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, IsUserOrReadOnlyPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
