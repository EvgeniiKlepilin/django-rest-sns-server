from socialnetwork.likes.models import Like
from rest_framework import serializers

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created']

class LikeAggregateSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    id__count = serializers.IntegerField(read_only=True)