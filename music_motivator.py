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
import threading
from statistics import mean

# Open Spotify in Web Browser
# webbrowser.open("https://www.spotify.com")
# print("Opened Spotify In Web Browser")

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
print("Authenticated to Spotify")

# Wait 10 seconds for Web Browser to finish opening
# time.sleep(10)

# Search through devices for web player and transfer playback to that device
for device in sp.devices()['devices']:
    if "Web Player" in device['name']:
        sp.transfer_playback(device_id=device['id'], force_play=True)
        break
print("Set Active Playback Device")

# Initialize Serial Connection to Arduino
ser = serial.Serial('/dev/ttyACM1', 115200)
print("Initialized Serial Connection")

# Open songs CSV file
songs = pd.read_csv('songs.csv')
print("Read Songs File")

avg_bpm = 70

# Main execution loop
def play_song():
    global avg_bpm
    while True:
        # Read last sent BPM measurement
#         read = ser.readline().decode()
#         print(read)
        bpm = avg_bpm
        print("BPM is " + str(bpm))

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
        print("Chose Song ID " + song_id)

        # Add the song to spotify queue and play it starting at a random time
        sp.add_to_queue(song_id)
        time.sleep(0.5)
        sp.next_track()
        time.sleep(1)
        sp.seek_track(randint(20, 60) * 1000)

        # Wait 1 minute for next loop
        time.sleep(30)

def get_bpm():
    global avg_bpm
    
    num_samples = 25
    
    list = [70] * num_samples
    
    while True:
        read = ser.readline().decode()
#         print(read.strip())
        try:
            read = int(float(read.split()[1]))
        except:
            read = 70
        
        if read < 200:
            list.pop(0)
            list.append(read)
        
        avg_bpm = mean(list)
#         print("Average BPM " + str(avg_bpm))
        
if __name__ == "__main__":
    t1 = threading.Thread(target=get_bpm)
    t2 = threading.Thread(target=play_song)
    
    t1.start()
    t2.start()