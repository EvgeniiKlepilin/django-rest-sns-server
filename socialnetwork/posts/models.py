from django.db import models

class Post(models.Model):
    body = models.TextField(max_length=280)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['body']