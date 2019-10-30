from flask import Flask, request, render_template, url_for, redirect, session, send_from_directory
import os, json, requests, spotipy, pprint, time
import flaskapp.secret as secret
from operator import attrgetter
# import utils.(filename)
import dicttoxml, xmltodict

pp = pprint.PrettyPrinter()

app = Flask(__name__)
app.secret_key = secret.FLASK_SECRET

spot = None

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
      'favicon.ico')

@app.route('/')
def show_page():
    return render_template("index.html") 

@app.route('/logged')
def show_another():
    global spot
    # get the auth portion of url
    url = request.url_root+"logged"
    code = request.args['code']
    print("spotify code", code, url)

    # make a post to spotify auth
    tokens = get_spotify_token(code, url)

    print(tokens)

    # get the spotify auth related tokens
    access_token = tokens['access_token']
    session['token']=access_token
    spot = spotipy.Spotify(auth=access_token)
    user = spot.me()
    pp.pprint(user)
    username = user['id']

    session["user"] = username

    print(session)

    return render_template("location.html")

    # # use location data to make the weather api call
    # mapwords = get_weather_keyword(42.3601, -71.0589)

    # playlist_name = user['display_name'].split()[0]+"'s weather playlist"
    # userplay = spot.current_user_playlists()
    # exister = None
    # for d in userplay['items']:
    #     if d['name']==playlist_name:
    #         exister = d['id']
    #         break
    # if exister:
    #     print("exists")
    #     spot.user_playlist_unfollow(username, exister)

    # # use weather data to create a spotify playlist
    # playlist = spot.user_playlist_create(username, 
    #     playlist_name, 
    #     public=False)

    # genres = ['pop', 'hip-hop', 'edm', 'rock', 'alternative']
    # rec_params = {
    #     "target_tempo": mapwords["cloudCover"],  
    #     "target_valence": mapwords["visibility"],  
    #     "target_energy": mapwords["temperature"],  
    #     "target_danceability": mapwords["windSpeed"],  
    #     "target_instrumentalness": mapwords["precipProbability"], 
    #     "seed_genres": ",".join(genres), 
    #     "limit": 20
    # }

    # header= {"Authorization": "Bearer "+str(access_token)}
    # url = "https://api.spotify.com/v1/recommendations"
    # res = requests.get(url, headers=header, params=rec_params)
    # resTracks = res.json()
    
    # tracks = [d['id'] for d in resTracks['tracks']]
    # print(tracks)

    # playlist_id = playlist['id']

    # pp.pprint(playlist)
    # # tracks = []
    # spot.user_playlist_add_tracks(username, playlist_id, tracks)

    # # store the id of the playlist. use the playlist id to play on speaker
    # # playPlaylistOnBose(playlist_id)
    # url = "http://192.168.1.157:8090/select"
    # payloadLeft = '<ContentItem source="SPOTIFY" type="uri" location="spotify:playlist:'
    # payloadRight = '" sourceAccount="nav_suri" isPresetable="true"></ContentItem>'
    # payload = payloadLeft + playlist_id + payloadRight
    # try:
    #   res = requests.post(url, data=payload, timeout=3)
    # except requests.exceptions.Timeout:
    #   return redirect("https://open.spotify.com/playlist/" + playlist_id)

    # return "Hello"

@app.route('/location')
def getLocation():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))

    # use location data to make the weather api call
    global spot
    user = spot.me()
    mapwords = get_weather_keyword(lat, lon)
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

    sendNotificationToBose(mapwords['summary'])

    pp.pprint(mapwords)
    pp.pprint(rec_params)

    playlist_name = user['display_name'].split()[0]+"'s weather playlist"
    userplay = spot.current_user_playlists()
    exister = None
    for d in userplay['items']:
        if d['name']==playlist_name:
            exister = d['id']
            break
    if exister:
        print("exists")
        spot.user_playlist_unfollow(user['id'], exister)

    # use weather data to create a spotify playlist
    playlist = spot.user_playlist_create(user['id'], 
        playlist_name, 
        public=False)

    header= {"Authorization": "Bearer "+str(session['token'])}
    url = "https://api.spotify.com/v1/recommendations"
    res = requests.get(url, headers=header, params=rec_params)
    resTracks = res.json()
    
    tracks = [d['id'] for d in resTracks['tracks']]
    print(tracks)

    playlist_id = playlist['id']

    pp.pprint(playlist)
    # tracks = []
    spot.user_playlist_add_tracks(user['id'], playlist_id, tracks)

    session['playlist'] = playlist_id

    url = "http://192.168.1.157:8090/select"
    payloadLeft = '<ContentItem source="SPOTIFY" type="uri" location="spotify:playlist:'
    payloadRight = '" sourceAccount="nav_suri" isPresetable="true"></ContentItem>'
    payload = payloadLeft + playlist_id + payloadRight
    try:
        res = requests.post(url, data=payload, timeout=1)
        # Use soundtouch API to play the playlist*
    except requests.exceptions.Timeout:
        return redirect("https://open.spotify.com/playlist/" + playlist_id)

    # store the id of the playlist. use the playlist id to play on speaker
    # Display a page that asks for user location -> once received, redirect to /play
    return redirect(url_for("play"))

@app.route('/play')
def play():
    time.sleep(2)
    # -----
    boseInfo = getBoseInfo()
    url = "http://192.168.1.157:8090/now_playing"
    info = requests.get(url)
    data = info.content
    parsed_data = xmltodict.parse(data)
    # Variables for Music Info
    playlist_title = parsed_data['nowPlaying']['ContentItem']['itemName'],
    track = parsed_data['nowPlaying']['track'],
    artist = parsed_data['nowPlaying']['artist'],
    album = parsed_data['nowPlaying']['album'],
    art = parsed_data['nowPlaying']['art']['#text']
    # -----

    print(str(playlist_title)[2:-3])

    return render_template("play.html", 
        boseInfo=boseInfo,
        playlist_title=str(playlist_title)[2:-3],
        track=str(track)[2:-3],
        artist=str(artist)[2:-3],
        album=str(album)[2:-3],
        art=art
    ) 

def get_spotify_token(code, redirect_url):
    url = "https://accounts.spotify.com/api/token"
    payload = {"grant_type": "authorization_code", "code": code, "redirect_uri":redirect_url, 
        "client_id": secret.CLIENT, 
        "client_secret": secret.CLIENT_SECRET}
    res = requests.post(url, data=payload)
    resjson = res.json()
    print("RESPONSE FOR TOKEN REQUEST", resjson)
    return resjson

def get_weather_keyword(lat, lon):
    url = "https://api.darksky.net/forecast/"
    key = secret.DARKSKY_SECRET
    location = "/42.3601,-71.0589"
    res = requests.get(url + key + location)
    rd = res.json()
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

def weathermap(actual, m1, m2):
    return restrict(float(actual), m1, m2)/float(m2-m1)
    
def restrict(num, m1, m2):
    if num<m1: return m1
    if num>m2: return m2
    return num
# -- Bose Speaker Info and Play playlist

def getBoseInfo():
    url = "http://192.168.1.157:8090/info"
    info = requests.get(url)
    data = info.content
    parsed_data = xmltodict.parse(data)
    if parsed_data:
      return parsed_data['info']['name']
    else:
      return None

def getPlayingInfo():
    url = "http://192.168.1.157:8090/now_playing"
    info = requests.get(url)
    data = info.content
    parsed_data = xmltodict.parse(data)
    if parsed_data:
      playing_data = {
        "playlist_title": str(parsed_data['nowPlaying']['ContentItem']['itemName']),
        "track": str(parsed_data['nowPlaying']['track']),
        "artist": str(parsed_data['nowPlaying']['artist']),
        "album": str(parsed_data['nowPlaying']['album']),
        "art": str(parsed_data['nowPlaying']['art']['#text'])
      }
      print(playing_data)
      return playing_data
    else:
      return None

def sendNotificationToBose(message):
    url = "http://192.168.1.157:8090/speaker"
    appKey = "<app_key>" + secret.BOSE_SECRET + "</app_key>"
    audioUrl = "<url>https://freesound.org/data/previews/275/275571_4486188-hq.mp3</url>"
    service = "<service>What Does Your Weather Sound Like?</service>"
    reason = "<reason>" + message + "</reason>"
    vol = "<volume>50</volume>"
    payload = "<play_info>" + appKey + audioUrl + service + reason + vol + "</play_info>"
    res = requests.post(url, data=payload)
  
# -- Navigation for Bose Speaker --

@app.route('/navigate/next', methods=['GET'])
def moveToNextTrack():
  if request.method == 'GET':
    url = "http://192.168.1.157:8090/key"
    payloadLeft = '<key state="press" sender="Gabbo">'
    payloadRight = '</key>'
    payload = payloadLeft + "NEXT_TRACK" + payloadRight
    res = requests.post(url, data=payload)
    return ''
  else:
    return None

@app.route('/navigate/prev', methods=['GET'])
def moveToPrevTrack():
  if request.method == 'GET':
    url = "http://192.168.1.157:8090/key"
    payloadLeft = '<key state="press" sender="Gabbo">'
    payloadRight = '</key>'
    payload = payloadLeft + "PREV_TRACK" + payloadRight
    res = requests.post(url, data=payload)
    return ''
  else:
    return None

@app.route('/navigate/play', methods=['GET'])
def togglePlay():
  if request.method == 'GET':
    url = "http://192.168.1.157:8090/key"
    payloadLeft = '<key state="press" sender="Gabbo">'
    payloadRight = '</key>'
    payload = payloadLeft + "PLAY_PAUSE" + payloadRight
    res = requests.post(url, data=payload)
    return ''
  else:
    return None
