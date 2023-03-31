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

# Correct date format in df
df_kaspi['date'] = pd.to_datetime(df_kaspi['date'],format='%d-%m-%Y')
df_curr['day'] = pd.to_datetime(df_curr['day'],format='%d-%m-%Y')

# Delete the first column from the DataFrame
df_kaspi = df_kaspi.iloc[:, 1:]
# Delete the empty row from the DataFrame
df_kaspi = df_kaspi.drop(df_kaspi.index[0])

# Check
print(df_kaspi.head())
print(df_curr.head())
print(df_kaspi.dtypes)
print(df_curr.dtypes)






# # Connect data to the SQLite database
# con = sqlite3.connect(os.path.expanduser('~/Desktop/docs/kaspi_dm.db'))
# df_kaspi.to_sql('kaspi_dm',con1,index=False,if_exists='replace')

# # Create function 'select' with parameter 'sql'
# def select(sql, con):
#   """print the query result"""
#   return print(pd.read_sql(sql, con))