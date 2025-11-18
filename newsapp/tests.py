"""
Tests for the 'newsapp' API endpoints.
"""

from django.test import TestCase
from django.urls import reverse
from .models import Publisher, CustomUser, Article


class ArticleAPITest(TestCase):
    """
    Test suite for the Article API endpoints.
    """
    def setUp(self):
        """
        Set up the necessary objects for the API tests.

        This creates one publisher, one journalist, one reader,
        one approved article, and one draft article.
        """
        self.publisher = Publisher.objects.create(name="Test Publisher")
        self.journalist = CustomUser.objects.create_user(
            username="journalist",
            password="pass",
            role="journalist",
            email="j@example.com"
        )
        self.reader = CustomUser.objects.create_user(
            username="reader",
            password="pass",
            role="reader",
            email="r@example.com"
        )

        # Create one article that is approved (public)
        Article.objects.create(
            title="Public Article",
            content="Content here",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
        )

        # Create one article that is not approved (draft)
        Article.objects.create(
            title="Draft Article",
            content="Draft content",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

    def test_api_returns_only_approved(self):
        """
        Ensures the main article API endpoint only returns
        articles that have been marked as 'approved'.
        """
        url = reverse("api_articles")  # Assumes URL name is 'api_articles'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()

        # We created two articles, but only one was approved
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Public Article")
