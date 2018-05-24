# smb-portal
SaveMyByke portal





Steps for setting up SMB-Portal


   
1. initial an empty folder with `git init`

2. clone this repo with `git clone <repo address >`

3. install virtualenv with `pip install virtualenv`


2. create a virtual environment `virtualenv <virtual environment name >`.

3. locate and activate this environment `source activate`.

4. `pip install -r requirements.txt` in your shell/terminal.

**make sure u create a database and user name savemybike on a postgis enabled postgresql server** 


5. then run `python manage.py makemigrations` then `python manage.py migrate`


6. then run the server with the command `python manage.py runserver`


7. in your web browser enter 'localhost:8000/login'
