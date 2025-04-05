import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import spotify_credentials

# Define your Spotify Developer credentials
CLIENT_ID = 'spotify_credentials.CLIENT_ID'
CLIENT_SECRET = 'spotify_credentials.CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8888/callback/'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-modify-playback-state user-read-playback-state'))

# Function to convert URL to URI
def url_to_uri(url):
    match = re.match(r'https://open\.spotify\.com/(track|album|playlist|artist)/([a-zA-Z0-9]+)', url)
    if match:
        return f"spotify:{match.group(1)}:{match.group(2)}"
    else:
        raise ValueError("Invalid Spotify URL")

# Function to play a Spotify track
def play_track(spotify_url):
    spotify_uri = url_to_uri(spotify_url)
    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']
        sp.start_playback(device_id=device_id, uris=[spotify_uri])
        print("Playing song...")
    else:
        print("No active devices found")

# Function to stop playing
def stop_playback():
    sp.pause_playback()
    print("Playback paused.")

import socket

try:
    socket.gethostbyname('api.spotify.com')
    print("DNS resolution successful.")
except socket.gaierror:
    print("DNS resolution failed.")

# Example usage:
spotify_url = 'https://open.spotify.com/track/4jPy3l0RUwlUI9T5XHBW2m?si=32937fb5862844a8'
play_track(spotify_url)
import time
time.sleep(3)
# Call stop_playback to stop the playback
stop_playback()
