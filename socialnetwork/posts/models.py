from django.db import models

class Post(models.Model):
    body = models.TextField(max_length=280)

    class Meta:
        ordering = ['body']