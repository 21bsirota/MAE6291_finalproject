import webbrowser
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import serial
import math
from random import randint
import pandas as pd

# Open Spotify in Web Browser
webbrowser.open("https://www.spotify.com")

# Authenticate to Spotify API
load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = "http://127.0.0.1:3000",
    scope = "user-read-playback-state user-modify-playback-state"
))

# Wait 10 seconds for Web Browser to finish opening
time.sleep(10)

# Search through devices for web player and transfer playback to that device
for device in sp.devices()['devices']:
    if "Web Player" in device['name']:
        sp.transfer_playback(device_id=device['id'], force_play=True)
        break

# Initialize Serial Connection to Arduino
ser = serial.Serial('/dev/ttyACM0', 115200)

# Open songs CSV file
songs = pd.read_csv('songs.csv')

# Main execution loop
while True:
    # Read last sent BPM measurement
    bpm = int(ser.readline())

    # Constrain measurement to 60 - 179
    if bpm < 60:
        bpm = 60
    if bpm > 179:
        bpm = 179

    # Round the BPM measurement down to the nearest 10
    rounded = math.floor(bpm / 10) * 10

    # Pull a random song from the correct bucket
    num_songs = int(songs.at[0, str(rounded)])
    song_number = randint(1, num_songs)
    song_id = songs.at[song_number, str(rounded)]

    # Add the song to spotify queue and play it
    sp.add_to_queue(song_id)
    sp.next_track()

    # Wait 1 minute for next loop
    time.sleep(30)
