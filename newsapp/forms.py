"""
Django forms for the 'newsapp' application.

Provides a ModelForm for creating and updating Article instances.
"""

from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    """
    A ModelForm for creating or updating an Article.
    """
    class Meta:
        """
        Meta options for the ArticleForm.
        """
        model = Article
        fields = ["title", "content", "publisher", "approved"]
