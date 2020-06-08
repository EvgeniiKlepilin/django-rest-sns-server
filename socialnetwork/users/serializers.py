from socialnetwork.users.models import User
from socialnetwork.posts.models import Post
from socialnetwork.posts.serializers import PostSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    post_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined', 'post_set']
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1