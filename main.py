from flask import Flask, render_template, request
from artist_service import ArtistService
import json

service = ArtistService('db.csv')
app = Flask(__name__)

#Zadanie 1
@app.route('/artist-image/<name>')
def artist(name):
    return service.getImage(name)

#Zadanie 2
@app.route('/')
def home():
    url = request.base_url
    data = service.findAll(url)
    return render_template('pages/artists.html', items=data)


#Zadanie 3
@app.route('/artist/<artist>')
def artist_info(artist):
    data = service.find(artist)
    return render_template('pages/info.html', data=data)


#Zadanie 4
@app.route('/artist/<artist>/song/<id>')
def song_info(artist, id):
    data = service.find_song(artist, id)
    return render_template('pages/song.html', data=data)



if __name__ == '__main__':
    app.run(debug=True, port=5001)
