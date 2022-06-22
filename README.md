



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
4. Run the flask app ```export FLASK_APP=app.main && flask run --reload```

### Deployments

We use heroku to deploy the app




