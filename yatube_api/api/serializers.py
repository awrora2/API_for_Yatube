from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        read_only=False,
        slug_field='username',
        queryset=User.objects.all(), required=True,)

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        if user == following:
            raise serializers.ValidationError('Запрещена подписка')
        return data

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group
