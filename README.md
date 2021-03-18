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
POSTGRES_HOST=192.168.10.1
POSTGRES_PORT=5434
POSTGRES_DB=taskcamp
POSTGRES_USER=taskcamp
POSTGRES_PASSWORD=secret
MEMCACHED_LOCATION=192.168.10.1:11211
__EOF__
```
if you need a debug to be enabled
```shell
>>.env << __EOF__
DJANGO_DEBUG=True
__EOF__
```
5. create and run postgresql instance (if needed)
```shell
docker run -d --name taskcamp-postgres --hostname taskcamp-postgres \
    -p 5434:5432 --env-file .env postgres:13-alpine
```
5. export variables from .env file
```shell
export $(cat .env | xargs)
```
6. create a db (run migrations)
```shell
python3 manage.py migrate
```
7. compile messages
```shell
python3 manage.py compilemessages
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
python3 manage.py makemessages -a
python3 manage.py compilemessages
```

4. run
```shell
python3 manage.py runserver 0:8000
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