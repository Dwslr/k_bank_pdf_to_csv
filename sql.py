import sqlite3
import pandas as pd
# I dont know yet why I import numpy
import numpy as np
# Import os to create paths like this '~/Desktop/...'
# use code  os.path.expanduser('~/...')
import os


# Create DataFrame (df) from csv file
df_kaspi = pd.read_csv(os.path.expanduser('~/Desktop/docs/kaspi_output.csv'))
df_curr = pd.read_excel(os.path.expanduser('~/Desktop/docs/cur_rates_last_year.xlsx'))
df_ffin = pd.read_excel(os.path.expanduser('~/Desktop/docs/ffinkz_statement.xlsx'))

# print(df_ffin.columns)

# Drop column
cols_to_drop = [col for col in df_ffin.columns if col.startswith('amount_curr')]
df_ffin = df_ffin.drop(cols_to_drop, axis=1)

# Convert column in desired date format 
df_ffin[['date']] = df_ffin[['date']].apply(lambda x: pd.to_datetime(x, format='%Y.%m.%d %H:%M:%S').dt.strftime('%Y-%m-%d'))

# Correct date format in df
df_kaspi['date'] = pd.to_datetime(df_kaspi['date'],format='%d-%m-%Y')
df_curr['day'] = pd.to_datetime(df_curr['day'],format='%d-%m-%Y')
# df_ffin['date_op'] = pd.to_datetime(df_ffin['date_op'],format='%Y-%m-%d')
df_ffin['date'] = pd.to_datetime(df_ffin['date'],format='%Y-%m-%d')

# Delete the first column from the DataFrame
df_kaspi = df_kaspi.iloc[:, 1:]
# Delete the empty row from the DataFrame
df_kaspi = df_kaspi.drop(df_kaspi.index[0])
# df_ffin = df_ffin.drop(df_ffin.index[0])

# Check
# print(df_kaspi.head())
# print(df_curr.head())
# print(df_kaspi.dtypes)
# print(df_curr.dtypes)
# print(df_ffin.head())
# print(df_ffin .dtypes)

# Create a connection to the SQLite database
con = sqlite3.connect(os.path.expanduser('~/Desktop/docs/database_kc.db'))

# Create cursor object to execute SQL commands ???
# cursor = con.cursor()

# Convert the dataframes into SQLite tables using the to_sql method
df_kaspi.to_sql('kaspi',con,index=False,if_exists='replace')
df_curr.to_sql('curr',con,index=False,if_exists='replace')
df_ffin.to_sql('ffin',con,index=False,if_exists='replace')

# Create function 'select' with parameter 'sql'
def select(sql):
  """print the query result"""
  return print(pd.read_sql(sql, con))

# sql = '''
# SELECT k.date, IIF(amount < 0, ROUND(amount / rate_rub_kzt, 0), NULL) AS outcome_rub, IIF(amount > 0, ROUND(amount / rate_rub_kzt, 0), NULL) AS income_rub
# FROM kaspi AS k
# JOIN curr AS c ON k.date = c.day
# '''

# sql ='''
# SELECT strftime('%Y-%m', date), SUM(outcome_rub), SUM(income_rub)
# FROM (SELECT k.date, IIF(amount < 0, ROUND(amount / rate_rub_kzt, 0), NULL) AS outcome_rub, IIF(amount > 0, ROUND(amount / rate_rub_kzt, 0), NULL) AS income_rub
#     FROM kaspi AS k
#     JOIN curr AS c ON k.date = c.day)
# GROUP BY 1
# ORDER BY 1 DESC
# '''

sql = '''
SELECT *
FROM ffin AS f'''

select(sql)