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

    # make a post to spotify auth

    # get the spotify auth related tokens

    # use location data to make the weather api call

    # us weather data to create a spotify playlist 
    return "Hello"