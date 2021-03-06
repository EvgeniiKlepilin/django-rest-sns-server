from django.utils import timezone
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken

class RequestTimeLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = None
        auth = None

        try:
            auth = authentication.JWTAuthentication().authenticate(request)
        except InvalidToken as e:
            auth = None
        
        if auth:
            user = auth[0]
            
        if user and user.is_authenticated:
            user.last_request = timezone.now()
            user.save()
        response = self.get_response(request)
        return response