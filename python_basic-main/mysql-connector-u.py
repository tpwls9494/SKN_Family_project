# pip install mysql-connector-python

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="squirrel",
    password="squirrel",
    database="menudb"
)

cursor = connection.cursor()

sql = "UPDATE tbl_menu SET menu_name = %s, menu_price = %s WHERE menu_code = 1"
values = ("쌀국수", 8500)

# sql = "REPLACE INTO tbl_menu(menu_code, menu_name, menu_price, category_code, orderable_status) VALUES (%s, %s, %s, %s, %s)"
# values = (104, '김치볶음밥', 10000, 4, 'Y')

cursor.execute(sql, values)
connection.commit()

print(f'{cursor.rowcount}개의 행을 업데이트하였습니다.')

cursor.close()
connection.close()