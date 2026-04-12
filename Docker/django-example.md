# Django Docker Examples

Django is a popular Python web framework. This guide shows how to containerize Django applications with PostgreSQL, Redis, and Nginx.

---

## Example 1: Basic Django + PostgreSQL Setup

### Project Structure
```
django-project/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── myapp/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
└── db/
    └── init.sql
```

### Step 1: Create Dockerfile
**Dockerfile**
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
```

### Step 2: Create requirements.txt
**requirements.txt**
```
Django==4.2.0
psycopg2-binary==2.9.6
djangorestframework==3.14.0
django-cors-headers==3.14.0
python-decouple==3.8
redis==4.5.5
celery==5.3.1
```

### Step 3: Create docker-compose.yml
**docker-compose.yml**
```yaml
version: '3.8'

services:
  # Database Service
  db:
    image: postgres:15-alpine
    container_name: django-postgres
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: django_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - django-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U django_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Django Web Service
  web:
    build: .
    container_name: django-app
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 4"
    ports:
      - "8000:8000"
    environment:
      DEBUG: 'False'
      ALLOWED_HOSTS: 'localhost,127.0.0.1'
      DB_ENGINE: 'django.db.backends.postgresql'
      DB_NAME: 'django_db'
      DB_USER: 'django_user'
      DB_PASSWORD: 'django_password'
      DB_HOST: 'db'
      DB_PORT: '5432'
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      db:
        condition: service_healthy
    networks:
      - django-network
    restart: on-failure

  # Redis Cache Service
  redis:
    image: redis:7-alpine
    container_name: django-redis
    ports:
      - "6379:6379"
    networks:
      - django-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  django-network:
    driver: bridge
```

### Step 4: Update Django settings.py
**myproject/settings.py (key sections)**
```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Redis Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Step 5: Run the Application
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access application
# Web: http://localhost:8000
# Admin: http://localhost:8000/admin

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

---

## Example 2: Django with Gunicorn + Nginx + PostgreSQL

### Production-Ready Setup with Nginx Reverse Proxy

### Project Structure
```
django-project/
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── myproject/
├── docker-compose.yml
└── entrypoint.sh
```

### Step 1: Nginx Configuration
**nginx/nginx.conf**
```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name localhost;
    client_max_body_size 10M;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location /admin/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**nginx/Dockerfile**
```dockerfile
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
EXPOSE 80
```

### Step 2: Django Dockerfile (Production)
**app/Dockerfile**
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Use entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
```

### Step 3: Entrypoint Script
**entrypoint.sh**
```bash
#!/bin/sh
set -e

# Wait for database
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "Database is ready"

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn myproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 60 \
    --keep-alive 5
```

### Step 4: docker-compose.yml (Production)
**docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: django-postgres-prod
    environment:
      POSTGRES_DB: ${DB_NAME:-django_db}
      POSTGRES_USER: ${DB_USER:-django_user}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-django_password}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - django-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-django_user}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: ./app
    container_name: django-app-prod
    environment:
      DEBUG: 'False'
      ALLOWED_HOSTS: 'localhost,127.0.0.1'
      DB_ENGINE: 'django.db.backends.postgresql'
      DB_NAME: ${DB_NAME:-django_db}
      DB_USER: ${DB_USER:-django_user}
      DB_PASSWORD: ${DB_PASSWORD:-django_password}
      DB_HOST: db
      DB_PORT: 5432
      SECRET_KEY: ${SECRET_KEY:-your-secret-key-change-in-production}
    expose:
      - 8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      db:
        condition: service_healthy
    networks:
      - django-network
    restart: on-failure

  nginx:
    build: ./nginx
    container_name: django-nginx-prod
    ports:
      - "80:80"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web
    networks:
      - django-network
    restart: on-failure

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  django-network:
    driver: bridge
```

---

## Example 3: Django with Celery + RabbitMQ + PostgreSQL

### Async Tasks Setup

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: django-postgres-celery
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: django_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - django-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U django_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: django-rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    ports:
      - "5672:5672"
      - "15672:15672"        # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - django-network
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: django-redis-celery
    networks:
      - django-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: django-app-celery
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8000:8000"
    environment:
      DEBUG: 'False'
      DB_HOST: db
      DB_NAME: django_db
      DB_USER: django_user
      DB_PASSWORD: django_password
      CELERY_BROKER_URL: amqp://guest:guest@rabbitmq:5672//
      CELERY_RESULT_BACKEND: redis://redis:6379
    volumes:
      - .:/app
    depends_on:
      db:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - django-network
    restart: on-failure

  celery:
    build: .
    container_name: django-celery-worker
    command: celery -A myproject worker -l info
    environment:
      DEBUG: 'False'
      DB_HOST: db
      DB_NAME: django_db
      DB_USER: django_user
      DB_PASSWORD: django_password
      CELERY_BROKER_URL: amqp://guest:guest@rabbitmq:5672//
      CELERY_RESULT_BACKEND: redis://redis:6379
    volumes:
      - .:/app
    depends_on:
      - db
      - rabbitmq
      - redis
      - web
    networks:
      - django-network
    restart: on-failure

  celery-beat:
    build: .
    container_name: django-celery-beat
    command: celery -A myproject beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    environment:
      DEBUG: 'False'
      DB_HOST: db
      DB_NAME: django_db
      DB_USER: django_user
      DB_PASSWORD: django_password
      CELERY_BROKER_URL: amqp://guest:guest@rabbitmq:5672//
      CELERY_RESULT_BACKEND: redis://redis:6379
    volumes:
      - .:/app
    depends_on:
      - db
      - rabbitmq
      - redis
    networks:
      - django-network
    restart: on-failure

volumes:
  postgres_data:
  rabbitmq_data:

networks:
  django-network:
    driver: bridge
```

### Django Celery Configuration
**myproject/settings.py (Celery config)**
```python
# Celery Configuration
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='amqp://localhost:5672//')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

**myproject/celery.py**
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**myapp/tasks.py**
```python
from celery import shared_task
import time

@shared_task
def send_email_task(email, subject, message):
    # Simulate email sending
    time.sleep(2)
    print(f"Email sent to {email}: {subject}")
    return f"Email sent to {email}"

@shared_task
def process_data_task(data):
    # Long-running task
    time.sleep(5)
    print(f"Processing data: {data}")
    return f"Data processed: {data}"
```

### Usage in Views
**myapp/views.py**
```python
from django.http import JsonResponse
from .tasks import send_email_task, process_data_task

def send_email_view(request):
    # Queue the task
    task = send_email_task.delay('user@example.com', 'Hello', 'Test message')
    return JsonResponse({'task_id': task.id, 'status': 'queued'})

def process_data_view(request):
    # Queue the task
    task = process_data_task.delay({'key': 'value'})
    return JsonResponse({'task_id': task.id, 'status': 'processing'})

def check_task_status(request, task_id):
    task = send_email_task.AsyncResult(task_id)
    return JsonResponse({
        'task_id': task_id,
        'status': task.status,
        'result': task.result
    })
```

### Run Celery
```bash
# Start all services including Celery
docker-compose up -d

# View Celery worker logs
docker-compose logs -f celery

# View Celery beat scheduler logs
docker-compose logs -f celery-beat

# Access RabbitMQ Management UI
# http://localhost:15672 (guest/guest)
```

---

## Example 4: Multi-Stage Build (Optimized Django)

**Dockerfile (Multi-stage)**
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages from wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Quick Start Commands

```bash
# Create Django project inside container
docker-compose run web django-admin startproject myproject .

# Create Django app
docker-compose run web python manage.py startapp myapp

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Create migrations
docker-compose exec web python manage.py makemigrations

# Django shell
docker-compose exec web python manage.py shell

# View database
docker-compose exec db psql -U django_user -d django_db

# Stop and remove all
docker-compose down -v
```

---

## Key Points for Django Docker

✅ **Use environment variables** for configuration  
✅ **Set PYTHONUNBUFFERED=1** to see logs immediately  
✅ **Use Gunicorn** in production (not Django development server)  
✅ **Use Nginx** as reverse proxy in production  
✅ **Use volumes** for persistent data  
✅ **Health checks** ensure proper startup order  
✅ **Use separate Dockerfile stages** for smaller images  
✅ **Run migrations** automatically in entrypoint  
✅ **Collect static files** before running production server  
✅ **Use non-root user** for security  
