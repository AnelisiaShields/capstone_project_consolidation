
# Simple Dockerfile for a Django app
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/
# Collect static files (if used)
# RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "news_capstone.wsgi:application", "--bind", "0.0.0.0:8000"]
