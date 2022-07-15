

import os

import sqlalchemy
from .utils import get_db_dynamic_url
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging


if (os.getenv('FLASK_ENV') == 'production'):
  # Fetch postgres DB URL
  SQLALCHEMY_DATABASE_URL = get_db_dynamic_url(os.getenv('HEROKU_APP_NAME', 'shiny-dandelion'))
  print(SQLALCHEMY_DATABASE_URL)

else:
  # Sqlite connection string - for testing purposes
  SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


logging.getLogger(__name__).info('DB URL: %s', SQLALCHEMY_DATABASE_URL)

# mysql connection has specific connection params
if SQLALCHEMY_DATABASE_URL.find('postgres') != -1 :
  engine = create_engine(SQLALCHEMY_DATABASE_URL )

else:
  engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
  )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()