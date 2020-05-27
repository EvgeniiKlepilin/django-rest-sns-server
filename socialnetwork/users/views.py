from django.http import Http404
from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from socialnetwork.users.models import User
from socialnetwork.users.serializers import UserSerializer

class UserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # permissions: IsAuthenticated
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # permissions: AllowAny
        return self.create(request, *args, **kwargs)

class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # permissions: IsAuthenticated
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # permissions: OnlySelf or IsAdmin
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # permissions: IsAdmin
        return self.destroy(request, *args, **kwargs)