from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import (Comment,
                          Post,
                          Follow,
                          Group)


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Follow
        fields = (
            'user',
            'following',
        )
        read_only_fields = (
            'user',
        )

    def get_user(self, obj):
        return obj.user.username


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'slug',
            'description',

        )
        read_only_fields = (
            'id',
        )


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'image',
            'group'
        )
        read_only_fields = (
            'id',
            'author',
            'pub_date',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created',
            'post'
        )
        read_only_fields = (
            'id',
            'author',
            'created',
            'post',
        )
