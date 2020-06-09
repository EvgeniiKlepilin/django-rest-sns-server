from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from socialnetwork.likes import views

urlpatterns = [
    path('analytics/', views.LikeList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)