# Taskcamp

[![Unittests with coverage](https://github.com/iliadmitriev/taskcamp/actions/workflows/django.yml/badge.svg)](https://github.com/iliadmitriev/taskcamp/actions/workflows/django.yml)
[![Build docker and push](https://github.com/iliadmitriev/taskcamp/actions/workflows/docker-build-and-push.yml/badge.svg)](https://github.com/iliadmitriev/taskcamp/actions/workflows/docker-build-and-push.yml)
[![codecov](https://codecov.io/gh/iliadmitriev/taskcamp/branch/master/graph/badge.svg?token=5YUABNBEZ5)](https://codecov.io/gh/iliadmitriev/taskcamp)

This software is used for educational and demonstrative purposes.
It's a simple project management tool powered by [Django Framework](https://www.djangoproject.com)

- [Install](#install)
  * [Bare metal install](#bare-metal-install)
  * [Docker install](#docker-install)
    + [Prepare](#prepare)
    + [Build and run](#build-and-run)
    + [Clean up](#clean-up)
  * [Docker-compose install](#docker-compose-install)
- [Development](#development)
- [Testing](#testing)
  * [Run tests](#run-tests)
  * [Run tests with coverage](#run-tests-with-coverage)

Features:
* Class-Based Views approach
* Login, Sign Up, Recover (LoginView, FormView, UserCreationForm, PasswordResetForm, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)
* Custom Extended User model (AbstractUser, BaseUserManager, UserManager)
* Permissions and Groups (LoginRequiredMixin, PermissionRequiredMixin)
* Simple CRUD views (ListView, DetailView, CreateView, UpdateView, DeleteView)
* File uploading
* Statistics (TemplateView, View, Q, F, Count, FloatField, Cast, Case, When, Sum, Avg)
* Forms (Form, ModelForm)
* Admin page (ModelAdmin, TabularInline)
* Template and layouts (include templates, blocks, custom 500, 404, 403 handlers)
* Router urls (include, namespace, params)
* Caching (memcached)
* Async workers with celery
* Localization and internationalization (with pluralization)
* Timezone support (pytz)
* Markdown syntax, Status highlight (Template tags)
* DB router (master, slave)
* Unittests with coverage
* Uwsgi (with static and media serving)
* Docker and docker-compose
* kubernetes deploy

Components:
* Database [PostgreSQL](https://www.postgresql.org)
* Cache [memcached](https://memcached.org)
* Application server [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/)
* Task queue [Celery](https://docs.celeryproject.org/en/stable/)
* Message Broker [RabbitMQ](https://www.rabbitmq.com)
* Localization [gettext](https://www.gnu.org/software/gettext/)
* Markup language [Markdown](https://python-markdown.github.io)
* Template Engine [Jinja2](https://jinja.palletsprojects.com/)
* Debugging, profiling and optimizing [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)

# Install

---

Types of installation

1. [Bare metal](#bare-metal-install)
2. [Docker](#docker-install)
3. [Docker-compose](#docker-compose-install)
4. [Kubernetes](kubernetes/README.md)

## Bare metal install

1. install python3 and create virtual env
```shell
python3 -m venv venv
source venv/bin/activate
```
2. install requirements
```shell
pip install -r requirements.txt
```
3. put django secret key into file .env
generate DJANGO_SECRET_KEY
```shell
echo DJANGO_SECRET_KEY=\'$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')\'  > .env
```
or just create test
```shell
echo DJANGO_SECRET_KEY=test_secret_key  > .env
```
4. add connection data to `.env` file
```shell
cat > .env << __EOF__
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taskcamp
POSTGRES_USER=taskcamp
POSTGRES_PASSWORD=secret

MEMCACHED_LOCATION=localhost:11211

EMAIL_HOST=localhost
EMAIL_PORT=1025
__EOF__
```
```shell
# if you need a debug be enabled
cat >>.env << __EOF__
DJANGO_DEBUG=True
__EOF__

#if you need to keep celery results 
>>.env << __EOF__
REDIS_RESULTS_BACKEND=redis://localhost:6379/0
__EOF__
```
5. create and run postgresql, memcached, mailcatcher and rabbitmq instance (if needed)
```shell
docker run -d --name taskcamp-postgres --hostname taskcamp-postgres \
    -p 5432:5432 --env-file .env postgres:alpine
    
docker run -d -p 11211:11211 --name taskcamp-memcached memcached:alpine

docker run -d -p 15672:15672 -p 5672:5672 \
  --name taskcamp-rabbit --hostname taskcamp-rabbit \
  --env-file .env rabbitmq:management-alpine

docker run -d -p 1080:1080 -p 1025:1025 \
 --name taskcamp-mailcatcher iliadmitriev/mailcatcher
```
```shell
# if you enabled REDIS_RESULTS_BACKEND to store celery results
docker run -d --name taskcamp-redis --hostname taskcamp-redis \
 -p 6379:6379 redis:alpine
```

5. export variables from .env file
```shell
export $(cat .env | xargs)
```
6. create a db (run migrations)
```shell
python3 manage.py migrate --no-input
```
7. compile messages
```shell
python3 manage.py compilemessages -i venv
```
8. create superuser
```shell
python3 manage.py createsuperuser
```

## Docker install

### Prepare

1. create `.env` file
```shell
>.env << __EOF__
RABBITMQ_HOST=taskcamp-rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery

POSTGRES_HOST=taskcamp-postgres
POSTGRES_PORT=5432
POSTGRES_DB=taskcamp
POSTGRES_USER=taskcamp
POSTGRES_PASSWORD=secret

MEMCACHED_LOCATION=taskcamp-memcached:11211
REDIS_RESULTS_BACKEND=redis://taskcamp-redis:6379/0

EMAIL_HOST=taskcamp-mail
EMAIL_PORT=1025
__EOF__
```

2. create network `taskcamp-network`
```shell
docker network create taskcamp-network
```

3. create docker containers (this is just an example, you shouldn't run in production like this)
```shell
docker run -d --name taskcamp-postgres --hostname taskcamp-postgres \
    --env-file .env --network taskcamp-network postgres:14-alpine
    
docker run -d --name taskcamp-memcached --hostname taskcamp-memcached \
    --network taskcamp-network memcached:alpine

docker run -d \
  --name taskcamp-rabbitmq --hostname taskcamp-rabbitmq \
  --env-file .env --network taskcamp-network \
  rabbitmq:management-alpine

docker run -d --name taskcamp-mail --hostname taskcamp-mail \
  --network taskcamp-network -p 1080:1080 iliadmitriev/mailcatcher
 
docker run -d --name taskcamp-redis --hostname taskcamp-redis \
  --network taskcamp-network redis:alpine
```

### Build and run
1. build docker image `taskcamp-python`
```shell
docker build -t taskcamp-python -f Dockerfile ./
```

2. run django web application
```shell
docker run -p 8000:8000 --env-file=.env -d --name=taskcamp-django \
  --hostname=taskcamp-django --network taskcamp-network taskcamp-python
```

3. run celery
```shell
docker run --env-file=.env -d --name=taskcamp-celery --hostname=taskcamp-celery \
   --network taskcamp-network taskcamp-python python3 -m celery -A worker worker
```

4. apply migrations
```shell
docker run --env-file=.env --rm -ti --network taskcamp-network taskcamp-python \
    python3 manage.py migrate
```

5. create superuser
```shell
docker run --env-file=.env --rm -ti --network taskcamp-network taskcamp-python \
    python3 manage.py createsuperuser
```

### Clean up
```shell
docker rm -f $(docker ps --filter name=^taskcamp -a -q)
docker network rm taskcamp-network
docker rmi taskcamp-python
```

## Docker-compose install

1. create `.env` environment variables file
```shell
>.env << __EOF__
RABBITMQ_HOST=taskcamp-rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery

POSTGRES_HOST=taskcamp-postgres
POSTGRES_PORT=5432
POSTGRES_DB=taskcamp
POSTGRES_USER=taskcamp
POSTGRES_PASSWORD=secret

MEMCACHED_LOCATION=taskcamp-memcached:11211
REDIS_RESULTS_BACKEND=redis://taskcamp-redis:6379/0

EMAIL_HOST=taskcamp-mail
EMAIL_PORT=1025
__EOF__
```

2. start docker-compose services
```shell
docker-compose up -d
```

3. apply migrations
```shell
docker-compose exec django python3 manage.py migrate
```

4. create superuser
```shell
docker-compose exec django python3 manage.py createsuperuser
```

5. load test data if needed
```shell
cat data.json | docker-compose exec -T django python3 manage.py loaddata --format=json - 
```

Docker-compose clean up

```shell
docker-compose down --rmi all --volumes
```

# Development

---
1. set environment variables
```shell
DJANGO_DEBUG=True
```

2. make migrations and migrate
```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

3. make messages
```shell
python3 manage.py makemessages -a -i venv
python3 manage.py compilemessages -i venv
```

4. run
```shell
python3 manage.py runserver 0:8000
```

5. run celery for emails and other async tasks
```shell
python3 -m celery -A worker worker
# or
celery -A worker worker
```

5. run celery for emails and other async tasks
```shell
python3 -m celery -A worker worker
```
or
```shell
celery -A worker worker
```
with log level and queue
```shell
celery -A worker worker -l INFO -Q email
```

# Testing

## Run tests 

1. run all tests
```shell
python3 manage.py test
```
2. run with keeping db in case of test fails
```shell
python3 manage.py test --keepdb
```
3. run all tests with details
```shell
python3 manage.py test --verbosity=2
```

## Run tests with coverage

1. run with coverage
```shell
coverage run manage.py test --verbosity=2
```
2. print report with missing lines and fail with error in case it's not fully covered
```shell
coverage report -m --fail-under=100
```
