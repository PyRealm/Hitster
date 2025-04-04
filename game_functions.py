def stop_game(players_timeline):
    for i in range(len(players_timeline)):
        if len(players_timeline[i])==10:
            return True
    return False
def current_player_timeline(players_timeline):
    t=[]
    result=[]
    helper1=0
    helper2=0
    for i in range(len(players_timeline)+1):
        t.append(i)
    for j in range(len(players_timeline)*2+1):
        if j%2!=0:
            result.append(players_timeline[helper1])
            helper1+=1
        else:
            result.append(t[helper2])
            helper2+=1
    return result
def show_current_players_timeline(current_players_timeline):
    for i in range(len(current_players_timeline)):
        if i%2==0:
            print(current_players_timeline[i]+1)
        else:
            print("   ",current_players_timeline[i][0],current_players_timeline[i][1],current_players_timeline[i][2])
def is_correct_answer(players_timeline,guess,correct_year):
    if guess==0:
        # print('check 1')
        if correct_year<=players_timeline[1][0]:
            return True
        return False
    elif guess==players_timeline[len(players_timeline)-1]:
        # print('check 2')
        if players_timeline[len(players_timeline)-2][0]<=correct_year:
            return True
        return False
    else:
        # print('check 3')
        for i in range(len(players_timeline)):
            if players_timeline[i]==guess:
                helper=i
                break
        if players_timeline[i-1][0]<=correct_year<=players_timeline[i+1][0]:
            return True
        return False
def add_song(players_timeline,year,title,author):
    helper=players_timeline
    helper.append([year,title,author])
    added= sorted(helper, key=lambda x: x[0])
    return added
def starting_timelines(players_timeline,players_quantity, previous_songs):
    from song_randomizer import random_song
    for i in range(players_quantity):
        helper=random_song(previous_songs)
        year, title, author, sound=helper.split(';')
        players_timeline[i].append([year,title,author])
