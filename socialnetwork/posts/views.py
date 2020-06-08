from django.http import Http404
from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from socialnetwork.posts.models import Post
from socialnetwork.posts.serializers import PostSerializer
from socialnetwork.posts.permissions import IsOwnerOrAdmin

class PostList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PostDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrAdmin
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostLike(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = self.get_object()
        instance.liked_by.add(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        instance = self.get_object()
        instance.liked_by.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)