from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from socialnetwork.posts import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/likes/', views.PostLike.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)