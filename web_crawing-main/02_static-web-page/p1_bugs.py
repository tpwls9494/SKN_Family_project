import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from urllib.request import urlretrieve

class BugsEntry:
    def __init__(self, title, artist, img_path):
        self.title = title
        self.artist = artist
        self.img_path = img_path

    def __repr__(self):
        return  f'{self.artist}, artist={self.title}, img_path={self.img_path}'
    
response = requests.get("https://music.bugs.co.kr/chart")
bs = BeautifulSoup(response.text, 'html.parser')

track_list = bs.select('table.trackList tbody tr')

print(track_list)

result_list = []
for i, song in enumerate(track_list[:30]):
    title = song.select_one('p.title a').text
    artist = song.select_one('p.artist a').text

    # print(title, artist)
    img_src = song.select_one('a.thumbnail img')['src']
    filename = f"album_images/{dt.now().strftime('%y%m%d_%H%M%S')}_{i + 1}.jpg"
    urlretrieve(img_src, filename)

    music_entry = BugsEntry(title, artist, filename)
    result_list.append(music_entry)

for result in result_list:
    print(result)