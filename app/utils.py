import subprocess


# Returns a heroku app database URL. 
# NOTE: A heroku token must be available as env var HEROKU_API_KEY. The
# token can be created by using heroku cli command: heroku authorizations:create

def get_db_dynamic_url(app_name):
  raw_url = subprocess.run(
    ['heroku', 'config:get', 'DATABASE_URL', '--app', app_name], capture_output=True).stdout
  
  raw_url_decoded = raw_url.decode('ascii').strip()

  return "postgresql+psycopg2://" + raw_url_decoded.lstrip('postgres://')
