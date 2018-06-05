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
    py.test --flake8
```

The `setup.cfg` file has some relevant settings for running tests. Be sure to 
check it out too
