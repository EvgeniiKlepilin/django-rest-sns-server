from socialnetwork.posts.models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'body', 'author', 'liked_by']
        depth = 1