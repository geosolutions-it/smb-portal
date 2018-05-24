# smb-portal
SaveMyByke portal





Steps for setting up SMB-Portal


   
1. initialize  an empty folder with `git init`

2. clone this repo with `git clone <repo address>`

3. install virtualenv with `pip install virtualenv`


4. create a virtual environment `virtualenv <virtual environment name>`.

5. locate and activate this environment `source activate`.

6. `pip install -r requirements.txt` in your shell/terminal.



7.if postgresql isnt installed. download and install from the official website

8. rename the local_sample.py.sample to local_sample.py

9. write your down database setting in the local_sample.py

8. then run `python manage.py makemigrations` then `python manage.py migrate`


9. then run the server with the command `python manage.py runserver`


10. in your web browser enter 'localhost:8000'
