# install

---

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
echo DJANGO_SECRET_KEY=\'$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')\'  >> .env
```
or just create test
```shell
echo DJANGO_SECRET_KEY=test_secret_key  >> .env
```
4. add connection data to `.env` file
```shell
>>.env << __EOF__
RABBITMQ_HOST=192.168.10.1
RABBITMQ_PORT=5673
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=adminsecret
RABBITMQ_DEFAULT_VHOST=celery

POSTGRES_HOST=192.168.10.1
POSTGRES_PORT=5434
POSTGRES_DB=taskcamp
POSTGRES_USER=taskcamp
POSTGRES_PASSWORD=secret

MEMCACHED_LOCATION=192.168.10.1:11214
__EOF__
```
if you need a debug to be enabled
```shell
>>.env << __EOF__
DJANGO_DEBUG=True
__EOF__

if you need to keep celery results 
>>.env << __EOF__
REDIS_RESULTS_BACKEND=redis://192.168.10.1:6380/0
__EOF__
```
5. create and run postgresql, memcached, mailcatcher and rabbitmq instance (if needed)
```shell
docker run -d --name taskcamp-postgres --hostname taskcamp-postgres \
    -p 5434:5432 --env-file .env postgres:13-alpine
    
docker run -d -p 11214:11211 --name taskcamp-memcached memcached:alpine

docker run -d -p 15673:15672 -p 5673:5672 \
  --name taskcamp-rabbit --hostname taskcamp-rabbit \
  --env-file .env rabbitmq:3.8.14-management-alpine

docker run -d -p 1080:1080 -p 1025:1025 \
 --name taskcamp-mailcatcher mailcatcher
```
if you need to store celery results
```shell
docker run -d --name taskcamp-redis --hostname taskcamp-redis \
 -p 6380:6379 redis:alpine
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
python3 manage.py compilemessages -i venv --no-input
```
8. create superuser
```shell
python3 manage.py createsuperuser
```

# development

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
python3 -m celery -A worker.app worker
# or
celery -A worker.app worker
```

5. run celery for emails and other async tasks
```shell
python3 -m celery -A worker.app worker
# or
celery -A worker.app worker
```
with log level and queue
```shell
celery -A worker.app worker -l INFO -Q activation_email
```

# testing

## run tests 

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

## run tests with coverage

1. run with coverage
```shell
coverage run manage.py test
```
2. print report with missing lines and fail with error in case it's not fully covered
```shell
coverage report -m --fail-under=100
```