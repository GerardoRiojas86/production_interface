import subprocess
import heroku3
import pandas as pd

# Returns a heroku app database URL. 
# NOTE: A heroku token must be available as env var HEROKU_API_KEY. The
# token can be created by using heroku cli command: heroku authorizations:create

def get_db_dynamic_url(app_name, api_key):

  heroku = connect_to_heroku(api_key)

  heroku_app = heroku.apps()[app_name]

  raw_url = heroku_app.config()['DATABASE_URL']

  return "postgresql+psycopg2://" + raw_url.lstrip('postgres://')
  
  # raw_url = subprocess.run(
  #   ['heroku', 'config:get', 'DATABASE_URL', '--app', app_name], capture_output=True).stdout
  
  # raw_url_decoded = raw_url.decode('ascii').strip()

  # return "postgresql+psycopg2://" + raw_url_decoded.lstrip('postgres://')


def connect_to_heroku(key):
  return heroku3.from_key(key)


# A Query class used to export Sqlalchemy queries into Pandas dataframes
class Query():

  def __init__(self, query=None, conn=None):
    self.query = query
    self.conn = conn
    pass
  
  def to_df(self):
    if (self.query != None and self.conn != None):
      return pd.read_sql_query(
            sql= self.query.statement,
            con=self.conn)
  
    else:
      return None
