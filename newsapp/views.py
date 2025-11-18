"""
Django views and API endpoints for the 'newsapp' application.

Provides function-based views for rendering article lists and details,
and a class-based API view for listing approved articles.
"""

from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from rest_framework import generics, permissions

from .models import Article
from .serializers import ArticleSerializer


def index(request: HttpRequest) -> HttpResponse:
    """
    Displays a list of all approved articles, ordered by creation date.

    :param request: The HttpRequest object.
    :return: An HttpResponse rendering the article list page.
    """
    articles = Article.objects.filter(approved=True).order_by("-created_at")
    context = {"articles": articles}
    return render(request, "newsapp/article_list.html", context)


def detail(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Displays the detail page for a single, approved article.

    :param request: The HttpRequest object.
    :param pk: The primary key of the article.
    :return: An HttpResponse rendering the article detail page.
    """
    article = get_object_or_404(Article, pk=pk, approved=True)
    context = {"article": article}
    return render(request, "newsapp/article_detail.html", context)


class ArticleListAPI(generics.ListAPIView):
    """
    API endpoint to list all approved articles.

    Supports optional query parameters:
    - ?publisher=<id>: Filter articles by publisher ID.
    - ?journalist=<id>: Filter articles by author/journalist ID.
    """
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Returns a queryset of approved articles, optionally filtered.
        """
        publisher_id = self.request.query_params.get("publisher")
        journalist_id = self.request.query_params.get("journalist")

        # Start with the base queryset of approved articles
        qs = Article.objects.filter(approved=True)

        # Apply optional filters
        if publisher_id:
            qs = qs.filter(publisher__id=publisher_id)
        if journalist_id:
            qs = qs.filter(author__id=journalist_id)

        return qs.order_by("-created_at")