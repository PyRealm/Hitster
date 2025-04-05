import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
import time
import requests.exceptions
import socket
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

def get_devices_with_retry(sp, retries=5, delay=2):
    for i in range(retries):
        try:
            devices = sp.devices()
            return devices
        except requests.exceptions.RequestException as e:
            # print(f"Attempt {i + 1} failed: {e}")
            if isinstance(e, requests.exceptions.ConnectionError):
                print("DNS resolution failed. Retrying...")
                try:
                    # Retry DNS resolution
                    socket.gethostbyname('api.spotify.com')
                except socket.gaierror as dns_error:
                    print(f"DNS resolution error: {dns_error}")
            time.sleep(delay)
    raise Exception("Failed to get devices after multiple retries")

# Function to play a Spotify track
def play_song(spotify_url):
    spotify_uri = url_to_uri(spotify_url)
    devices = get_devices_with_retry(sp)
    if devices['devices']:
        device_id = devices['devices'][0]['id']
        sp.start_playback(device_id=device_id, uris=[spotify_uri])
        # print("Playing song...")

# Function to check if Spotify track is playable
def play_song_test(spotify_url):
    try:
        spotify_uri = url_to_uri(spotify_url)
        if 'spotify:track:' not in spotify_uri:
            # print("Unsupported URI kind: only track URIs are supported.")
            return False

        devices = get_devices_with_retry(sp)
        if devices['devices']:
            # print("Playing song...")
            return True
        else:
            # print("No active devices found")
            return False
    except ValueError as ve:
        # print(f"Error: {ve}")
        return False
    except spotipy.exceptions.SpotifyException as se:
        # print(f"Spotify API error: {se}")
        return False
    except Exception as e:
        # print(f"An unexpected error occurred: {e}")
        return False

# Function to stop playing
def stop_song(retries=5, delay=2):
    for i in range(retries):
        try:
            sp.pause_playback()
            # print("Playback paused.")
            return
        except spotipy.exceptions.SpotifyException as se:
            # print(f"Spotify API error on attempt {i + 1}: {se}")
            print("Poczekaj chwileczkę")
        except requests.exceptions.ReadTimeout as e:
            # print(f"Read timeout on attempt {i + 1}: {e}")
            print("Poczekaj chwileczkę")
        except requests.exceptions.RequestException as e:
            # print(f"Request exception on attempt {i + 1}: {e}")
            print("Poczekaj chwileczkę")
        time.sleep(delay)
    # print("Failed to stop playback after multiple retries.")
