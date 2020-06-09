from django.utils import timezone
from rest_framework_simplejwt import authentication

class RequestTimeLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = authentication.JWTAuthentication().authenticate(request)[0]
        if user.is_authenticated:
            user.last_request = timezone.now()
            user.save()
        response = self.get_response(request)
        return response