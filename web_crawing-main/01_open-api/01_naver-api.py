import urllib.request
# naver 크롤링

# API 호출을 위한 client_id, client_secret 변수 설정정
client_id = '1zV9pKtEq41EugdGx81i'
client_secret = 'LAe0rXNUxl'

encText = urllib.parse.quote('너를')

# 요청 URL
# url = "https://openapi.naver.com/v1/search/news.json?query=" + encText
# url2 = "https://openapi.naver.com/v1/search/news.xml?query=" + encText
url3 = "https://openapi.naver.com/v1/search/book.json?query=" + encText

# Request 객체 생성 -> 헤더 설정
request = urllib.request.Request(url3)
request.add_header('X-naver-Client-Id', client_id)
request.add_header('X-naver-Client-Secret', client_secret)

# 실제 요청 후 응답
response = urllib.request.urlopen(request)

# getcode() : 응답 코드 반환
print(response.getcode())

# read() : 응답 내용 반환
response_body = response.read()
print(response_body.decode('utf-8'))