from socialnetwork.posts.models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):

    # TODO: limit author to serialized fields
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'body', 'author']
        depth = 1