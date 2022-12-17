import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


class ArtistService:

    def __init__(self, fileName):
        self.db = pd.read_csv(fileName , encoding ='latin1')
        self.image_cache = {}

    def getImage(self, artistName):
        if not os.path.isdir('files'):
            os.mkdir('files')
        article_url = 'https://en.wikipedia.org/wiki/' + artistName

        if artistName in self.image_cache:
            return self.image_cache[artistName]

        response = requests.get(article_url)
        if response == None:
            return 'not found'

        soup = BeautifulSoup(response.text, 'html.parser')
        if soup == None:
            return 'not found'

        info_element = soup.find('table', class_='infobox')
        if info_element == None:
            return 'not found'

        image_element = info_element.find('img')
        if image_element == None:
            return 'not found'

        image_url = image_element['src']
        image_url = 'https:' + image_url;

        image_response = requests.get(image_url)
        path = os.path.join('files', artistName + '.jpg');
        if os.path.isfile(path):
            open(path, 'wb').write(image_response.content)
        self.image_cache[artistName] = image_url
        return image_url

    def findAll(self, url):
        df = self.db[['title', 'artist']]
        df = df.groupby('artist')
        result = []
        for name, group in df:
            artist = {}
            id = name.replace(" ", "_")
            artist["id"] = id
            artist["name"] = name
            artist["songs"] = len(group.values)
            artist['image'] = url+'artist-image/'+id
            if artist['songs'] == 1:
                artist['border'] = 'pink'
            else:
                artist['border'] = 'brown'

            result.append(artist)

        return result

    def find(self, id):

        artistName = id.replace("_", " ")
        df = self.db[['title', 'lyrics', 'language', 'year', 'artist','id']]
        df = df[df['artist'] == artistName]
        df = df.groupby('artist')

        artist = {}
        for name, group in df:
            id = name.replace(" ", "_")
            artist["id"] = id
            artist["artist"] = artistName
            artist["image"] = self.getImage(id)
            artist["songs"] = []
            for value in group.values:
               song = {}
               song['title'] = value[0]
               song['text'] = value[1]
               song['language'] = value[2]
               song['year'] = value[3]
               song['type'] = 'pop'
               song['id'] = value[5]
               artist["songs"].append(song)

        return artist

    def find_song(self, artist, songId):
        id = int(songId)
        df = self.db[['id','title', 'lyrics', 'artist']]
        df = df[df['id'] == id]

        row = df.iloc[0]
        song = {}
        song["artist"] = row['artist']
        song["title"] = row['title']
        song["text"] = row['lyrics']
        return song
