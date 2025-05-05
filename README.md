# This repository holds the code for Music Motivator
## This project was completed for the GWU course MAE 6291 in Spring 2025

---

The goal of this project was to create an IoT Thing that can read a person's heartbeat and play songs where the Tempo matches their current heartbeat. There is currently a preset list of songs that will play every 30 seconds (adjustable), starting at a random point in the middle of the song.

---

### To Use:
This code is designed to be used with an Arduino, a Raspberry Pi, and a [PulseSensor](https://pulsesensor.com/).
1. Clone this repository to your Raspberry Pi
2. Install the python modules listed in `requirements.txt`
```
pip install spotipy pyserial python-dotenv pandas
```
3. In the repository folder, create a file called `.env` that contains your Spotify Client ID and Client Secret. For example:
```
CLIENT_ID=AAAAAAAAA
CLIENT_SECRET=BBBBBBBBBB
```
4. Upload the code in `pulse_sensor.ino` to your Arduino using the Arduino IDE
5. Connect your PulseSensor to your Arduino
    - Red wire goes to `5V`
    - Black wire goes to `GND`
    - Purple wire goes to `A0`
6. Connect your speaker or other audio device to your Raspberry Pi
7. Run `music_motivator.py` on the Raspberry Pi

### Troubleshooting
- If you aren't consistently reading the heartbeat correctly (the built in LED on your arduino should light up with each beat), try adjusting the `threshold` parameter in `pulse_sensor.ino`.
- Make sure we are reading the right serial port in `music_motivator.py`. Sometimes the Arduino might connect to `/dev/ttyACM0` or another port. I'm not sure how to consistently tell what port it will connect to, but if the script gives a serial error, it might be this.
- If you have a low-end Raspberry Pi, it may take a while for spotify to open in the web browser, preventing the rest of the script from working correctly. In this case, it may be better to pre-open spotify before running the script and comment out `webbrowser.open("https://www.spotify.com")`.
- Make sure you are already logged into Spotify on your Raspberry Pi's web browser. You will only need to authenticate once, but it is best to complete this ahead of time.
- Make sure your spotify queue is empty/cleared before running, if not, the script will just go through your queue one at a time instead of playing the correct song.
- This code is tested using Python 3.9. Other versions may work but are untested.
- This code is tested with an Arduino Mega 2560. Other hardware may work but are untested.