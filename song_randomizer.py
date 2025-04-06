import random
import spotify_credentials

def random_song(previous_songs):
    with open(spotify_credentials.writing_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        random_number = -1
        while random_number in previous_songs or 'spotify:artist:' in lines[random_number]:
            random_number = random.randint(0, len(lines) - 1)
        previous_songs.append(random_number)
        return lines[random_number].strip()
