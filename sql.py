import sqlite3
import pandas as pd
# I dont know yet why I import numpy
import numpy as np
# Import os to create paths like this '~/Desktop/...'
# use code  os.path.expanduser('~/...')
import os


# Create DataFrame (df) from csv file
df_kaspi = pd.read_csv(os.path.expanduser('~/Desktop/docs/kaspi_output.csv'))
df_curr = pd.read_excel(os.path.expanduser('~/Desktop/docs/currs_12_04_23.xlsx'))
df_ffin = pd.read_excel(os.path.expanduser('~/Desktop/docs/ffinkz_statement_2.xlsx'))

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
cursor = con.cursor()

# Convert the dataframes into SQLite tables using the to_sql method
df_kaspi.to_sql('kaspi',con,index=False,if_exists='replace')
df_curr.to_sql('curr',con,index=False,if_exists='replace')
df_ffin.to_sql('ffin',con,index=False,if_exists='replace')

# Create function 'select' with parameter 'sql'
def select(sql):
  """print the query result"""
  return print(pd.read_sql(sql, con))


# delete table if it was created early
sql = '''
DROP TABLE IF EXISTS general;
'''
con.execute(sql)

# Union the two tables into one general statement
sql = '''
CREATE TABLE general AS
SELECT date, amount, note, ROUND(amount / c.rate_rub_kzt, 0) AS amount_r
FROM kaspi AS k
  JOIN curr AS c ON k.date = c.day
WHERE amount NOT IN (SELECT k.amount
                    FROM kaspi AS k
                      LEFT JOIN ffin AS f ON k.date = f.date
                    WHERE k.amount < 0 
                    AND k.note LIKE '%1402%' 
                    AND f.description LIKE '%p2p%' 
                    AND f.amount > 0 
                    AND ABS(k.amount) > f.amount * 0.9 
                    AND ABS(k.amount) < f.amount * 1.1
                    )
UNION ALL
SELECT date, amount, description, ROUND(amount / c.rate_rub_kzt, 0) AS amount_r
FROM ffin AS f
  JOIN curr AS c ON f.date = c.day
WHERE amount NOT IN (SELECT f.amount
                    FROM ffin AS f
                      LEFT JOIN kaspi AS k ON f.date = k.date
                    WHERE f.amount < 0 
                    AND f.description LIKE "%P2P%" 
                    AND k.operation = "Пополнение"
                    )
'''

con.execute(sql)

# sql = '''
# SELECT *
# FROM general
# '''
# select(sql)

# select sum and max expenses grouping by month
sql = '''
SELECT STRFTIME('%Y-%m', g.date) AS month, 
        SUM(amount_r) AS sum_expense_r,
        MIN(amount_r) AS max_expense_r,
        g.note
FROM general AS g
WHERE amount < 0
GROUP BY 1
ORDER BY 1 DESC
'''
#select(sql)

# 
sql = '''
SELECT STRFTIME('%Y-%m', g.date) AS month,
        amount_r AS big_expense_r,
        g.note
FROM general AS g
WHERE amount_r < (SELECT AVG(amount_r) AS avg_expense_r
                  FROM general AS g
                  WHERE amount_r < 0
                  ) * 5

ORDER BY 1 DESC, 2 
'''
#select(sql)

sql = '''
SELECT SUM(amount_r)
FROM general
WHERE amount_r > 0
'''

sql = '''
SELECT SUM(amount_r)
FROM general
WHERE amount_r < 0
'''

print('--------------------------------------------------------------------------------------------------------')
print('------------------------------------- FFIN')
sql = '''
SELECT STRFTIME('%Y-%m-%d', date) AS date_s, amount, description
FROM ffin
WHERE description LIKE '%p2p%'
'''
#select(sql)

print('--------------------------------------------------------------------------------------------------------')
print('------------------------------------- KASPI')
sql = '''
SELECT STRFTIME('%Y-%m-%d', date) AS date_s, amount, operation, note
FROM kaspi
WHERE operation LIKE 'Пополнение'
'''
#select(sql)

print('--------------------------------------------------------------------------------------------------------')
print('------------------------------------- GENERAL')
sql = '''
SELECT SUM(amount) / 6
FROM general
WHERE amount < 0
'''
#select(sql)

sql = '''
SELECT SUM(amount) / 6
FROM general
WHERE amount > 0
'''
#select(sql)

sql = '''
SELECT STRFTIME('%Y-%m-%d', date) AS date_s, amount, note, ABS(amount)
FROM general
WHERE note LIKE '%p2p%' OR note LIKE '%карт%' OR note LIKE '%номеру счета%'
ORDER BY 1 DESC, 4 DESC
'''
sql = '''
SELECT *
FROM (SELECT STRFTIME('%Y-%m-%d', date) AS date_s, amount, note, ABS(amount)
      FROM general
      WHERE note LIKE '%p2p%' OR note LIKE '%карт%' OR note LIKE '%номеру счета%'
      ORDER BY 1 DESC, 4 DESC
      )
WHERE date_s > '2023-02-01' AND date_s < '2023-02-31'
'''
#select(sql)

sql = '''
SELECT STRFTIME('%Y-%m', date) AS month, SUM(ABS(amount_r)) AS sum_expence_r
FROM general AS g
WHERE amount < 0
GROUP BY 1
ORDER BY 1 DESC
'''
select(sql)