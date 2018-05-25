# smb-portal

Steps for setting up this project:

*  clone this repo

*  create a virtual environment and name it smbportal.

*  activate this environment.

*  `pip install -r requirements/production.txt` in your shell/terminal.

*  make sure to create a database and user name savemybike on a postgis enabled postgresql server** 

*  then run `python manage.py makemigrations` then `python manage.py migrate`

*  then run the server with the command `python manage.py runserver`

*  in your web browser enter 'localhost:8000/login'
