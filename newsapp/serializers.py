"""
Serializers for the 'newsapp' API.

Defines serializers for the Publisher and Article models,
converting them to and from JSON representations.
"""

from rest_framework import serializers
from .models import Article, Publisher


class PublisherSerializer(serializers.ModelSerializer):
    """
    Serializes Publisher model data.
    """
    class Meta:
        """
        Meta options for the PublisherSerializer.
        """
        model = Publisher
        fields = ["id", "name", "description"]


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializes Article model data.

    Uses StringRelatedField for 'author' to show the user's string
    representation.
    Uses a nested PublisherSerializer for 'publisher' to show
    full publisher details.
    """
    author = serializers.StringRelatedField()
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        """
        Meta options for the ArticleSerializer.
        """
        model = Article
        fields = [
            "id", "title", "content", "author", "publisher",
            "created_at", "approved"
        ]
