from socialnetwork.users.models import User
from socialnetwork.posts.serializers import PostSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1