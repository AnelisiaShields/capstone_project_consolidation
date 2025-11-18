"""
Django signals for the 'newsapp' application.

This module defines signal handlers that respond to model events.
"""

from typing import Set
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article, CustomUser


@receiver(post_save, sender=Article)
def article_approved_handler(
    sender,
    instance: Article,
    created: bool,
    **kwargs
):
    """
    Handles actions when an Article is saved.

    When an article's 'approved' status is changed to True,
    this signal notifies all subscribers of the associated
    publisher and the author.
    """
    # Exit if the 'approved' field is not True
    if not instance.approved:
        return

    # Check the "pre-save" state to see if 'approved' just changed.
    # This prevents sending emails on every save of an already-approved article.
    if not created:
        try:
            # Get the version of the object from the database
            old_instance = sender.objects.get(pk=instance.pk)
            # If it was already approved, do nothing.
            if old_instance.approved:
                return
        except sender.DoesNotExist:
            # This shouldn't happen on a post-save, but good to handle
            pass

    # --- At this point, the article was just approved ---
    subject = f"New article published: {instance.title}"
    message = instance.content[:200] + "..."

    # Use a sensible from_email fallback
    from_email = settings.DEFAULT_FROM_EMAIL or "no-reply@example.com"

    # Collect recipients: publisher subscribers and journalist subscribers
    recipients: Set[str] = set()

    # 1. Get subscribers to the publisher
    if instance.publisher:
        publisher_subs = instance.publisher.subscribers.all()
        recipients.update(
            u.email for u in publisher_subs if u.email
        )

    # 2. Get subscribers to the journalist (author)
    author_subs = instance.author.journalist_subscribers.all()
    recipients.update(
        u.email for u in author_subs if u.email
    )

    if recipients:
        send_mail(
            subject,
            message,
            from_email,
            list(recipients)
        )

    # TODO: post to X (Twitter) via its API - left as a stub
