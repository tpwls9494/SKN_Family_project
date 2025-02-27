# pip install mysql-connector-python

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="squirrel",
    password="squirrel",
    database="menudb"
)

if connection.is_connected():
    print("MySQL에 성공적으로 연결되었습니다.")

connection.close()