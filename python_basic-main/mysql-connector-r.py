# pip install mysql-connector-python

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="squirrel",
    password="squirrel",
    database="menudb"
)

cursor = connection.cursor()


# 커서 실행
cursor.execute("SELECT menu_code, menu_name, menu_price FROM tbl_menu")
result = cursor.fetchall()

for row in result:
    print("menucode:", row[0], '/', 'menuname:', row[1], '/', 'menuprice:', row[2])


# print(result)

cursor.close()

connection.close()