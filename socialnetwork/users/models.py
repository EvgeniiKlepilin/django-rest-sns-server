from django.db import models
from django.contrib.auth.models import AbstractUser
from socialnetwork.posts.models import Post

class User(AbstractUser):
    likes = models.ManyToManyField(Post, related_name="liked_by")
    last_request = models.DateTimeField(null=True, blank=True)