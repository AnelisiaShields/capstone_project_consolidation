"""
Database models for the 'newsapp' application.

Defines the data structure for:
- Publisher: An entity that publishes articles (e.g., a newspaper).
- CustomUser: An extended User model with roles (Reader, Editor, Journalist).
- Article: A news article written by a User.
"""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Define choices for the CustomUser.role field
ROLE_CHOICES = (
    ("reader", "Reader"),
    ("editor", "Editor"),
    ("journalist", "Journalist"),
)


class Publisher(models.Model):
    """
    Represents an organization that publishes articles.
    (e.g., "The Daily News").
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        ordering = ['name']

    def __str__(self):
        """
        Returns the string representation of the publisher (its name).
        """
        return self.name


class CustomUser(AbstractUser):
    """
    A custom user model extending AbstractUser.

    Includes a 'role' to differentiate between Readers, Editors,
    and Journalists, and fields for managing subscriptions.
    """
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader"
    )

    # --- Subscriptions for 'Reader' role ---
    subscriptions_publishers = models.ManyToManyField(
        Publisher,
        related_name="subscribers",
        blank=True
    )
    # A self-referential M2M for users to follow journalists
    subscriptions_journalists = models.ManyToManyField(
        "self",
        related_name="journalist_subscribers",
        blank=True,
        symmetrical=False  # If you follow a journalist, they don't follow you
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        """
        Overrides the save method.

        Currently contains placeholder logic to enforce role-based
        field constraints.
        """
        # Enforce fields based on role
        if self.role == "journalist":
            # Placeholder for future validation logic
            pass
        super().save(*args, **kwargs)

    # --- Properties for easy role checking ---
    @property
    def is_reader(self):
        """Returns True if the user is a reader."""
        return self.role == "reader"

    @property
    def is_editor(self):
        """Returns True if the user is an editor."""
        return self.role == "editor"

    @property
    def is_journalist(self):
        """Returns True if the user is a journalist."""
        return self.role == "journalist"


class Article(models.Model):
    """
    Represents a news article.

    An article is written by a User (author) and can be
    optionally associated with a Publisher.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Correctly references CustomUser
        on_delete=models.CASCADE,
        related_name="articles"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,  # Allows articles from independent journalists
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns the string representation of the article (its title).
        """
        return self.title
