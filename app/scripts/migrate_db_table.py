from venv import create
from sqlalchemy import create_engine
import pandas as pd

# Script that connects to a database via db_uri
# allowing to fetch data, process and import.

# Database connection string
db_uri = ""

engine = create_engine(db_uri, echo=False)

# Origin and target table names
origin_table = ''
target_table = ''

# Read origin table data and keep it in a dataframe
data_df = pd.read_sql_table(origin_table, con=engine)


# Modify, process the data
data_df['model'] = data_df['model'].apply(lambda x: x.upper())
data_df['project_id'] = 1

del data_df['project']
del data_df['updated_at']
del data_df['id']

print(data_df)


# Import the data into the target table
# use the 'append' technique
try:
  data_df.to_sql(target_table, con=engine, if_exists='append', index=False)
  print('Data imported!')
except Exception as e:
  print('Unable to import data: %s', e)



