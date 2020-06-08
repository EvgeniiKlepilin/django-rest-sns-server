from socialnetwork.users.models import User
from socialnetwork.posts.models import Post
from socialnetwork.posts.serializers import PostSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined', 'posts', 'likes']
        extra_kwargs = {'password': {'write_only': True}, 'books': {'required': False}}
        depth = 1