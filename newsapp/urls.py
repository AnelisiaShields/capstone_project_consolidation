from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("article/<int:pk>/", views.detail, name="article_detail"),
    path("api/articles/", views.ArticleListAPI.as_view(), name="api_articles"),
]
