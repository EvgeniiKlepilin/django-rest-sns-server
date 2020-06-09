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

    def update(self, instance, validated_data):
        User.objects.filter(pk=instance.id).update(**validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'date_joined', 'posts', 'likes']
        extra_kwargs = {'password': {'write_only': True}, 'books': {'required': False}}
        depth = 1

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'last_request']
        extra_kwargs = {'last_login': {'read_only': True}, 'last_request': {'read_only': True}}