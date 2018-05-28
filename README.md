# smb-portal

Steps for setting up this project:

*  Create a postgis database

*  clone this repo

*  create a virtual environment and activate it

*  `pip install -r requirements/production.txt` in your shell/terminal.

*  Ensure you have all the variables defined in `deployment/demo.env`,
   (with appropriate values) in your environment and that they will be 
   exported to child processes. 
   You can define local variables inside "deployment/local.env". local.env is gitignored

*  Run `python manage.py migrate` in order to have the DB structure be created

*  Run the server with the command `python manage.py runserver 0:8000`

*  in your web browser enter 'localhost:8000'
