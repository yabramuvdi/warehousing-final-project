import mysql.connector
import pandas as pd

db_username = "awesometeam"
db_password = "nandan123"
db_name = "test"
db_endpoint = "big-apple.cbx9jy53wa9n.us-east-2.rds.amazonaws.com"

#RDS configuration settings
config = {
  'user': db_username,
  'port': '3306',
  'password': db_password,
  #RDS instace endpoint
  'host': db_endpoint,
  'database': db_name,
  'raise_on_warnings': True
}

#Setup the connector
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def calls_data():
    cursor.execute("SELECT * FROM 311_calls")
    df_calls = pd.DataFrame(cursor.fetchall())

    cursor.execute('SHOW COLUMNS FROM 311_calls')
    columns = cursor.fetchall()
    column_names = [c[0] for c in columns]
    df_calls.columns = column_names
    return(df_calls)
