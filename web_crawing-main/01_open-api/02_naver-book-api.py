import urllib.parse
import urllib.request
import json
import mysql.connector

# 클라이언트 정보
client_id = '1zV9pKtEq41EugdGx81i'
client_secret = 'LAe0rXNUxl'

# 가져올 입력값
searchText = urllib.parse.quote('소나기')

# url 위치
url = "https://openapi.naver.com/v1/search/book.json?query=" + searchText + '&display=100'

# request header에 클라이언트 id pw 추가가
request = urllib.request.Request(url)
request.add_header('X-naver-Client-Id', client_id)
request.add_header('X-naver-Client-Secret', client_secret)

# 실제 요청 후 응답
response = urllib.request.urlopen(request)
response_body = response.read()
response_body = json.loads(response_body) # json을 사용하기 위해 response_body를 만듦

###############################################################################################################
# SQL

book_list = response_body['items']

# SQL 연결결
connection = mysql.connector.connect(
    host="localhost",
    user="squirrel",
    password="squirrel",
    database="bookdb"
)

cursor = connection.cursor()

# sql에 넣을 구문
sql = 'INSERT INTO naver_book (book_title, book_image, author, publisher, isbn, book_description, pub_date) VALUES (%s, %s, %s, %s, %s, %s, %s)'

for book_info in book_list:
    values = (book_info['title'], book_info['image'], book_info['author'], book_info['publisher'], book_info['isbn'], book_info['description'], book_info['pubdate'])
cursor.execute(sql, values)

connection.commit()

cursor.close()
connection.close()