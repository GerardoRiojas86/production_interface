



## Pre-requisites

* mysql server
  
  For Mac OS install and run mysql with commands

  ```sh
    brew install mysql
    brew services start mysql

    # connect to localhost and create database. By default root password is set
    # to blank
    mysql -u root -p 
    
    mysql> CREATE DATABASE flaskcontacts;
  ```

* Python 3.10.4
  

## Development

> Make sure to run mysql service

1. Create a python virtual environment with command ```python -m venv venv```
2. Upgrade pip with command ```pip install --upgrade pip```
3. Install python requirements via ```pip install -r requirements```
4. Run the flask app ```flask run --reload```

### Deployments

To deploy the app (in heroku):
1. Install heroku cli
2. Deploy main branch to heroku with command
   ```git push heroku main```

   Deploy ANY branch to heroku with command
   ```git push heroku your-branch-name:main```
   
The following files are required to deploy the app in Heroku:
* Procfile, defines the app python process and how it will be run
* runtime.txt, set the python version used to deploy the app
* app/wsgi.py, flask app executor used in combination with gunicorn 


