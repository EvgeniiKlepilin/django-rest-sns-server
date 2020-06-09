from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from socialnetwork.users.models import User
from rest_framework import status

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        user = User.objects.get(username=request.data["username"])
        update_last_login(None, user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)