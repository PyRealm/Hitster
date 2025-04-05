import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_credentials

# Spotify API credentials
CLIENT_ID = spotify_credentials.CLIENT_ID
CLIENT_SECRET = spotify_credentials.CLIENT_SECRET

# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

def display_tracks_info(tracks):
    songs = []
    for idx, item in enumerate(tracks):
        track = item['track']
        track_name = track.get('name', 'Unknown Title')
        artist_name = track['artists'][0].get('name', 'Unknown Artist')
        release_date = track['album'].get('release_date', 'Unknown Date')
        spotify_url = track['external_urls'].get('spotify', 'No URL')
        
        if release_date and '-' in release_date:
            release_year = release_date.split('-')[0]
            songs.append([release_year, track_name, artist_name, spotify_url])
        else:
            release_year = 'Unknown'

    return songs

def write_to_file(songs, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for song in songs:
            release_year, track_name, artist_name, spotify_url = song
            file.write(f"{release_year};{track_name};{artist_name};{spotify_url}\n")

if __name__ == '__main__':    
    tracks = get_playlist_tracks(spotify_credentials.playlist_id)
    if not tracks:
        print("Nie znaleziono żadnych utworów w tej playliście.")
    else:
        print(f"Znaleziono {len(tracks)} utworów w playliście.")
    songs = display_tracks_info(tracks)
    songs_in_order= sorted(songs, key=lambda x: x[0], reverse=True)
    write_to_file(songs_in_order, spotify_credentials.writing_path)
    print('Dane zostały poprawnie zapisane')
