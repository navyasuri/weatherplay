# musicformyhead.space
A real-time weather-based Spotify playlist generator for your Bose speakers. Project for HackGT 2019.

## Inspiration
Seasonal Affective Disorder (SAD) is a phenomenon that we have personally faced and know is a widespread issue, especially on college campuses where students may not be used to the climate of their school.  Recent studies have shown promise in the area of utilizing music therapy to treat various types of depression, and we wanted to develop a web application that could help anyone use music as a tool for acclimating and persevering by fetching weather data and control the playing of the resulting customized playlist on any Bose speaker. We wanted to also create a seamless experience for the user, with as little steps as possible to get an appropriate set of tracks playing. Hence we tried to create a UX that requires very little interaction from the user - just getting permissions and access. 

## What We Learned
The team members as a whole took on the task of building out the frontend and backend to ensure smooth functionality and elegant UX.  We learned how to utilize the Transposit environment to more rapidly condense API calls. Alexa had to learn SQL and work on modifying and implementing the DarkSky API for geolocation and weather data. Alexa also worked on identifying specific pieces of weather data (for instance, cloud cover) that would correlate well to characteristics of songs (for instance, valence -- which is another word for positivity). Navya and Alexa figured out how to map these to one another. 

Rick and Navya both spent a ton of time becoming intimately familiar with the playlist and song portions of the Spotify API. Rick also learned how to control the Bose Soundtouch speaker with our code. Navya learned how to deploy the entire app on Google Cloud and point our domain to it! We also listened to a lot of new songs and playlists while prototyping that we are excited to listen to and share!

## How We Built It
Weather data (from current location) --> Dark Sky API, SQL, JavaScript

Playlist creation --> Spotify API, Python

Playing songs --> Bose Soundtouch API, Spotify API

Web application --> Flask, JavaScript, Google Cloud (for hosting), Domain.com (for domain)

## Challenges We Faced
The weather data provided was actually too voluminous, and we had to parse through it in order to filter out irrelevant data. We played around with mapping different weather data to different audio attributes until we were satisfied with the results. Testing this was time-consuming. 

We also dealt with bugs that created additional playlists every time someone tried to request one from the same location but edited it so that new playlists would replace old ones (unless someone is following the playlist, then they still have access to it). It was our first time using sessions with Flask, and it was fun to figure that out. 

## We're Excited About...
Personalized, smart playlists and the power they have to uplift and empathize with users! With more time, we would have loved to be able to create the same experience for non-Spotify users and provide options for more customization if users choose. (And singing karaoke as a team.)
