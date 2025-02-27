import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlretrieve

class MusicEntry:
    def init(self, title, artist, img_path):
        self.title = title
        self.artist = artist
        self.img_path = img_path

    def repr(self):
        return f'{self.artist}의 {self.title} | {self.img_path}'

# request 로 url get해오기
response = requests.get('https://music.bugs.co.kr/chart')

# response를 html 로 받기 -> BeautifulSoup 객체 생성
bs = BeautifulSoup(response.text, 'html.parser')

# table.trackList 목록 > a.thumbnail img: 앨범커버 이미지, p.title a text: 앨범 제목
track_list = bs.select('table.trackList tbody tr')

result_list = []
for i, song in enumerate(track_list[:30]):  # 30개로 슬라이싱, enumerate 인터럴하게 인덱스를 받아올 수 있음
    title = song.select_one('p.title a').text
    artist = song.select_one('p.artist a').text
    # print(title, artist) -> 중간 점검 출력용

    # 4. 앨범커버 이미지 저장
    img_src = song.select_one('a.thumbnail img')['src']
    filename = f'albumimages/{datetime.now().strftime('%y%m%d%H%M%S')}_{i+1}.jpg'
    urlretrieve(img_src, filename)

    music_entry = MusicEntry(title, artist, filename)
    result_list.append(music_entry)


# 30위까지 출력
for result in result_list:
    print(result)