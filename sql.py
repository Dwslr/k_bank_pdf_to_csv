import sqlite3
import pandas as pd
# I dont know yet why I import numpy
import numpy as np
# Import os to create paths like this '~/Desktop/...'
# use code  os.path.expanduser('~/...')
import os


# Create DataFrame (df) from csv file
df = pd.read_csv(os.path.expanduser('~/Desktop/docs/kaspi_output.csv'))

# print(df.head())

# Correct date format in df
df['date'] = pd.to_datetime(df['date'],format='%d-%m-%Y')
# print(df.dtypes)

# Delete the first column from the DataFrame
df = df.iloc[:, 1:]

# Delete the empty row from the DataFrame
df = df.drop(df.index[0])

# Connect data to the SQLite database
con = sqlite3.connect(os.path.expanduser('~/Desktop/docs/kaspi_dm.db'))
df.to_sql('kaspi_dm',con,index=False,if_exists='replace')

# Create function 'select' with parameter 'sql'
def select(sql):
  """print the query result"""
  return print(pd.read_sql(sql,con))

# Declaration parameter
sql = '''
SELECT *
FROM kaspi_dm
'''
#Function call
select(sql)