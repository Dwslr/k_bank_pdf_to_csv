import sqlite3
import pandas as pd
# I dont know yet why I import numpy
import numpy as np
# Import os to create paths like this '~/Desktop/...'
# use code  os.path.expanduser('~/...')
import os


# Create DataFrame (df) from csv file
df_kaspi = pd.read_csv(os.path.expanduser('~/Desktop/docs/kaspi_output.csv'))

# print(df.head())

# Correct date format in df
df_kaspi['date'] = pd.to_datetime(df_kaspi['date'],format='%d-%m-%Y')
# print(df.dtypes)

# Delete the first column from the DataFrame
df_kaspi = df_kaspi.iloc[:, 1:]

# Delete the empty row from the DataFrame
df_kaspi = df_kaspi.drop(df_kaspi.index[0])

# Connect data to the SQLite database
con1 = sqlite3.connect(os.path.expanduser('~/Desktop/docs/kaspi_dm.db'))
df_kaspi.to_sql('kaspi_dm',con1,index=False,if_exists='replace')

# Create function 'select' with parameter 'sql'
def select(sql, con):
  """print the query result"""
  return print(pd.read_sql(sql, con))

# Declaration parameter
# sql = '''
# SELECT STRFTIME("%Y-%m", date) AS year_month, SUM(amount)
# FROM kaspi_dm AS t
# WHERE amount > 0
# GROUP BY 1
# ORDER BY 1 DESC
# '''

#Function call
# select(sql)

# Create DataFrame (df) from excel file with currencies
df_curr = pd.read_excel(os.path.expanduser('~/Desktop/docs/cur_rates_last_year.xlsx'))

df_curr['day'] = pd.to_datetime(df_curr['day'],format='%d-%m-%Y')
# print(df_curr.dtypes)
# print(df_curr.head())

# Connect data from currencies DataFrame to the SQLite database
con2 = sqlite3.connect(os.path.expanduser('~/Desktop/docs/curr.db'))
df_curr.to_sql('curr',con2,index=False,if_exists='replace')

sql = '''
SELECT *
FROM kaspi_dm'''

select(sql, con1)

sql = '''
SELECT *
FROM curr'''

select(sql, con2)
