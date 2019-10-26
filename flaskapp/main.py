from flask import Flask, request, render_template, url_for
import os
# import utils.(filename)

app = Flask(__name__)

@app.route('/')
def show_page(): 
    return render_template("index.html") 

@app.route('/other')
def show_another():
    # get the auth portion of url
    read_auth()

    # make a post to spotify auth

    # get the spotify auth related tokens

    # use location data to make the weather api call
    keywords = get_weather_keyword(lat, lon)

    # use weather data to create a spotify playlist
    
    # store the id of the playlist. use the playlist id to play on speaker
    
    return "Hello"

def get_weather_keyword(lat, lon):
    pass
    url = ""
    params = {"lat": "", "lon": ""}
    # res = requests.get(url, params=params)
    # print(res.json)
    summary = ""
    return summary