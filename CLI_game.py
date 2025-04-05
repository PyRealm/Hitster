from song_player import play_song
from song_player import stop_song
from song_randomizer import random_song
from game_functions import stop_game
from game_functions import current_player_timeline
from game_functions import show_current_players_timeline
from game_functions import is_correct_answer
from game_functions import add_song
import os
import time 


os.system('cls')
welcome_text='Hitster by Aleksander Wanot'
print(welcome_text.center(120))

players_count=int(input("Ilu graczy bierze udział? "))
players_names=[]
players_timeline=[[] for _ in range(players_count)]
previous_songs=[-1]
current_player=0
current_round=1

for i in range(players_count):
    imie=input(f"Podaj imię {i+1} gracza: ")
    players_names.append(imie)

for j in range(players_count):
    helper=random_song(previous_songs)
    year, title, author, sound=helper.split(';')
    players_timeline[j].append([year,title,author])

game_stopper=stop_game(players_timeline)

while game_stopper!=True:
    os.system('cls')
    round_text="Tura " + str(current_round)
    print(round_text.center(120))
    player_text="Kolejka " + players_names[current_player]
    print(player_text.center(120))

    round_players_timeline=current_player_timeline(players_timeline[current_player])
    show_current_players_timeline(round_players_timeline)

    song_player=input("\nKliknij enter aby puścić piosenkę")

    year,title,author,song=random_song(previous_songs).split(';')
    play_song(song)
    print()
    guess = int(input("Podaj miejsce w którym powinna się znaleźć obecnie grana piosenka: "))
    while guess<0 or guess>round_players_timeline[len(round_players_timeline)-1]+1:
        print("Wprowadzono liczbę spoza dostępnych w Twojej osi czasu")
        guess = int(input("Podaj liczbę która znajduje się w Twojej osi czasu: "))
    guess-=1

    if is_correct_answer(round_players_timeline,guess,year)==True:
        print("Prawidłowa odpowiedź")
        print(f'To był utwór "{title}" wykonany przez {author} z roku {year}')
        players_timeline[current_player]=add_song(players_timeline[current_player],year,title,author)
    elif is_correct_answer(round_players_timeline,guess,year)==False:
        print("Zła odpowiedź")
        print(f'To był utwór "{title}" wykonany przez {author} z roku {year}')
    stop_song()

    game_stopper=stop_game(players_timeline)
    if game_stopper==True:
        winner=current_player
    time.sleep(5)
    if current_player+1==players_count:
        current_player=0
        current_round+=1
    elif current_player+1<players_count:
        current_player+=1
    os.system('cls')
    

os.system('cls')
final_text="Koniec gry"
print(final_text.center(120))
winner_text="Wygrał "+players_names[winner]
print(winner_text.center(120))
