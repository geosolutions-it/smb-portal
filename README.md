# smb-portal

Steps for setting up this project:

*  Create a postgis database

*  clone this repo

*  create a virtual environment and activate it

*  `pip install -r requirements/production.txt` in your shell/terminal.

*  Ensure you have all the variables defined in `deployment/demo.env`,
   (with appropriate values) in your environment and that they will be 
   exported to child processes. 

*  Run `python manage.py migrate` in order to have the DB structure be created

*  Run the server with the command `python manage.py runserver 0:8000`

*  in your web browser enter 'localhost:8000'


# Running tests

This project is using pytest for automated testing. For running tests you 
should install the development packages specified in `requirements/dev.txt`

```python
pip install -r requirements/dev.txt
```

For running tests you need a DB user that has sufficient permissions to create
a new database and for creating the `postgis` extension inside it.

```psql
CREATE USER test_user WITH PASSWORD 'some-password';
ALTER USER test_user SUPERUSER;
```

Then run tests with

```bash
DJANGO_DATABASE_URL="postgis://test_user:some-password@host:port/db" \
    py.test --flake8 -m 'not acceptance'
```

The `setup.cfg` file has some relevant settings for running tests. Be sure to 
check it out too


## Acceptance tests

Acceptance tests ensure the code meets the expectations. These use extra 
dependencies and do not require the portal code to be installed. Install 
dependencies by running:

```bash
pip install -r requirements/acceptance.txt
```

These tests perform browser automation. As such they also require a previous 
install of firefox and the [gecko driver](https://github.com/mozilla/geckodriver)

Run tests with (replace with meaningful values)

```bash
pytest \
    -x \
    --url=http://10.0.1.164:8000 \
    --keycloak-base-url=http://10.0.1.164:8180 \
    --keycloak-realm=demo \
    --keycloak-client-id=demoapp \
    --keycloak-admin=admin \
    --keycloak-password=123456 \
    tests/acceptancetests/
```
