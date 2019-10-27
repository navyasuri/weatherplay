from flask import Flask, request, render_template, url_for
import os, json, requests, spotipy, pprint
import flaskapp.secret as secret
from operator import attrgetter
# import utils.(filename)
import dicttoxml

pp = pprint.PrettyPrinter()

app = Flask(__name__)

spot = None

positionData = {}

@app.route('/')
def show_page(): 
    return render_template("index.html") 

@app.route('/logged')
def show_another():
    global spot
    # get the auth portion of url
    code = request.args['code']
    print("spotify code", code)

    # make a post to spotify auth
    tokens = get_spotify_token(code)


    # get the spotify auth related tokens
    access_token = tokens['access_token']
    spot = spotipy.Spotify(auth=access_token)
    user = spot.me()
    pp.pprint(user)
    username = user['id']

    # use location data to make the weather api call
    mapwords = get_weather_keyword(42.3601, -71.0589)

    # use weather data to create a spotify playlist
    playlist = spot.user_playlist_create(username, 
        user['display_name']+"'s mood playlist", 
        public=False)

    genres = ['pop', 'hip-hop', 'edm', 'rock', 'alternative']
    rec_params = {
        "target_tempo": mapwords["cloudCover"],  
        "target_valence": mapwords["visibility"],  
        "target_energy": mapwords["temperature"],  
        "target_danceability": mapwords["windSpeed"],  
        "target_instrumentalness": mapwords["precipProbability"], 
        "seed_genres": ",".join(genres), 
        "limit": 20
    }

    header= {"Authorization": "Bearer "+str(access_token)}
    url = "https://api.spotify.com/v1/recommendations"
    res = requests.get(url, headers=header, params=rec_params)
    resTracks = res.json()
    
    tracks = [d['id'] for d in resTracks['tracks']]
    print(tracks)


    playlist_id = playlist['id']

    pp.pprint(playlist)
    # tracks = []
    spot.user_playlist_add_tracks(username, playlist_id, tracks)

    # store the id of the playlist. use the playlist id to play on speaker

    # requests.post
    return "Hello"

def get_spotify_token(code):
    url = "https://accounts.spotify.com/api/token"
    payload = {"grant_type": "authorization_code", "code": code, "redirect_uri":"http://localhost:5000/logged", 
        "client_id": secret.CLIENT, 
        "client_secret": secret.CLIENT_SECRET}
    res = requests.post(url, data=payload)
    resjson = res.json()
    print("RESPONSE FOR TOKEN REQUEST", resjson)
    return resjson

def get_weather_keyword(lat, lon):
    url = "https://api.darksky.net/forecast/f8e4346a41cff3c66e447fd9bc38c543/42.3601,-71.0589"
    res = requests.get(url)
    rd = res.json()
    pp.pprint(rd)
    keywords = {
        "timezone": rd['timezone'], # String
        "summary": rd['currently']['summary'], 
        "cloudCover": restrict((150*(1-float(rd['currently']['cloudCover'])))+50, 50, 200), 
        "visibility": weathermap(rd['currently']['visibility'], 0, 10), 
        "temperature": weathermap(rd['currently']['temperature'], 0, 120), 
        "precipProbability": float(rd['currently']['precipProbability']), 
        "windSpeed": weathermap(rd['currently']['windSpeed'], 0, 40)
    }
    print(keywords)
    return keywords

def playBose(id):
    url = "http://192.168.1.157:8090/"
    info = requests.get(url + "info")
    print(info)


def weathermap(actual, m1, m2):
    return restrict(float(actual), m1, m2)/float(m2-m1)
    
def restrict(num, m1, m2):
    if num<m1: return m1
    if num>m2: return m2
    return num