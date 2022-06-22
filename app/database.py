from venv import create
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Sqlite connection string - for testing purposes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Mysql connection string
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1/flaskcontacts"

# mysql connection has specific connect
if SQLALCHEMY_DATABASE_URL.find('mysql') != -1 :
  engine = create_engine(SQLALCHEMY_DATABASE_URL )

else:
  engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
  )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()