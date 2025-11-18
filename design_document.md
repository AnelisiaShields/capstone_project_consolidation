# Design Document — News Application (Capstone)

## Overview

This document describes the architecture, data model, API design, UI/UX plan,
and deployment notes for the News Application required by the capstone.

## Functional Requirements

- Readers can view approved articles and subscribe to publishers or journalists.
- Journalists can create, update, and delete their own articles.
- Editors can approve articles; approved articles are emailed to subscribers and posted to X.
- REST API provides third-party clients with access to articles filtered by publisher or journalist.
- Authentication and permissions enforced via Django groups/roles.

## Data Model (ERD summary)

- `CustomUser` (extends AbstractUser) — role, subscriptions to publishers & journalists.
- `Publisher` — name, description, many-to-many to CustomUser via subscribers.
- `Article` — title, content, author (CustomUser), publisher (optional), approved flag.

## API Endpoints

- `GET /api/articles/` — list approved articles.
  - Query params: `publisher`, `journalist`
- Additional endpoints to implement: create/update/delete for authenticated roles.

## Workflow: Article approval

1. Journalist creates an article (approved=False).
2. Editor reviews article (editor UI) and sets `approved=True`.
3. A signal (`post_save`) triggers:
   - Emails sent to subscribers (publisher and journalist subscribers).
   - Post to X via API (requires credentials and secure storage).

## UI/UX

- Simple responsive list/detail views for readers.
- Admin/editor dashboard using Django admin or custom views.
- Newsletter subscription management page.

## Security & Permissions

- Use Django Groups: Reader, Journalist, Editor.
- Assign permissions:
  - Reader: view_article
  - Journalist: add/change/delete own articles
  - Editor: change/delete any article, approve articles

## Testing

- Unit tests for API (provided).
- Integration tests for signals and email delivery.
- Manual Postman collection for API acceptance testing.

## Deployment

- Use MariaDB in production. See `setup_mariadb.md` for recommended steps.
- Store secrets in environment variables and use `django-environ` or similar.

## Notes

This starter implements core models, a basic API, and signals. Expand on it
to fully satisfy the submission rubric (UI polish, complete permissions,
newsletter models, X integration, and comprehensive tests).
