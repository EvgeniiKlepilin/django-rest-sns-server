from django.http import Http404
from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from socialnetwork.posts.models import Post
from socialnetwork.posts.serializers import PostSerializer

class PostList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        # permissions: IsAuthenticated
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # permissions: IsAuthenticated
        return self.create(request, *args, **kwargs)

class PostDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        # permissions: IsAuthenticated
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # permissions: OnlySelf or IsAdmin
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # permissions: OnlySelf or IsAdmin
        return self.destroy(request, *args, **kwargs)