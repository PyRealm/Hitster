import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as simpledialog
import GUI_CSS
import time 

from song_player import play_song
from song_player import play_song_test
from song_player import stop_song
from song_randomizer import random_song
from game_functions import starting_timelines
from game_functions import add_song
from game_functions import is_correct_answer
from game_functions import current_player_timeline
from game_functions import stop_game

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Classes~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text:str="", radius=GUI_CSS.menu_button_radius, btnforeground=GUI_CSS.font, btnbackground=GUI_CSS.button, border_color=GUI_CSS.border, border_width=GUI_CSS.menu_button_border_width, buttonWidth=GUI_CSS.menu_button_width, buttonHeight=GUI_CSS.menu_button_height, clicked=None, *args, **kwargs):
        self.border_width = border_width
        self.border_color = border_color

        super(RoundedButton, self).__init__(master, width=buttonWidth + 2*border_width, height=buttonHeight + 2*border_width, *args, **kwargs)

        self.config(bg=self.master["bg"], highlightthickness=0)
        self.btnbackground = btnbackground
        self.clicked = clicked
        self.radius = radius

        # Draw border
        self.border_rect = self.round_rectangle(border_width, border_width, buttonWidth + border_width, buttonHeight + border_width, radius=radius, fill=border_color, outline="")

        # Draw button inside border
        self.button_rect = self.round_rectangle(border_width*2, border_width*2, buttonWidth, buttonHeight, radius=radius-border_width, fill=btnbackground, outline="")
        
        self.text = self.create_text((buttonWidth // 2 + border_width, buttonHeight // 2 + border_width), text=text, fill=btnforeground, font=(GUI_CSS.font_name, int(buttonHeight*0.35)), justify="center")
       
        # Bind the tags to the elements
        self.tag_bind(self.button_rect, "<ButtonPress-1>", self.on_click)
        self.tag_bind(self.button_rect, "<ButtonRelease-1>", self.on_release)
        self.tag_bind(self.button_rect, "<Enter>", self.on_hover)
        self.tag_bind(self.button_rect, "<Leave>", self.on_leave)
        
        self.tag_bind(self.text, "<ButtonPress-1>", self.on_click)
        self.tag_bind(self.text, "<ButtonRelease-1>", self.on_release)
        self.tag_bind(self.text, "<Enter>", self.on_hover)
        self.tag_bind(self.text, "<Leave>", self.on_leave)

        self.bind("<Configure>", self.resize)

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.create_polygon(points, **kwargs, smooth=True)

    def resize(self, event):
        pass  # Implement if needed

    def on_click(self, event):
        if self.clicked is not None:
            self.clicked()

    def on_release(self, event):
        self.itemconfig(self.button_rect, fill=self.btnbackground)

    def on_hover(self, event):
        self.itemconfig(self.button_rect, fill=GUI_CSS.hover)

    def on_leave(self, event):
        self.itemconfig(self.button_rect, fill=self.btnbackground)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Adding PLayers Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def players_number_input(entry, players_names, root, error_label):
    # Get the number of inputs from the entry
    players_quantity = entry.get().strip()

    if players_quantity.isdigit():
        players_quantity = int(players_quantity)
        clear_window(root)
        players_names_input(players_quantity, root, players_names)

    else:
        error_label.config(text="PODAJ PRAWIDŁOWĄ LICZBĘ")  # Display the error message

def players_names_input(players_quantity, root, players_names):
    clear_window(root)

    # Function to update the label dynamically based on player count
    def update_player_label(counter_value):
        # Create a label with the player number (counter_value + 1)
        button_label.config(text=f"Podaj imię {counter_value + 1} gracza")

    # Create a label
    button_label = tk.Label(root, text=f"Podaj imię 1 gracza", font=(GUI_CSS.font_name, 24), bg=GUI_CSS.main, fg=GUI_CSS.font)
    button_label.pack(pady=(GUI_CSS.menu_pady, GUI_CSS.pady))

    # Validation to limit the entry to 15 characters
    def validate_entry(text):
        return len(text) <= 15

    # Register validation command
    vcmd = (root.register(validate_entry), '%P')

    # Create a standard rectangular entry field with a pre-filled space
    players_name_entry = tk.Entry(root, font=(GUI_CSS.font_name, 20), bg=GUI_CSS.button, fg=GUI_CSS.font, justify="center", validate="key", validatecommand=vcmd)
    players_name_entry.pack(pady=GUI_CSS.pady)
    players_name_entry.focus_set()

    # Create a button to submit the input
    submit_players_name_button = RoundedButton(
        root, 
        text="DALEJ", 
        radius=GUI_CSS.menu_button_radius, 
        btnbackground=GUI_CSS.button, 
        btnforeground=GUI_CSS.font, 
        border_color=GUI_CSS.border, 
        border_width=GUI_CSS.menu_button_border_width, 
        buttonWidth=GUI_CSS.menu_button_width, 
        buttonHeight=GUI_CSS.menu_button_height, 
        clicked=lambda: add_to_players_names(players_name_entry, players_names, players_quantity, submit_players_name_button.counter, update_player_label)
    )
    submit_players_name_button.pack(pady=GUI_CSS.pady)

    # Function to simulate the button click
    def simulate_button_click(event=None):
        submit_players_name_button.clicked()

    # Bind the Enter key (Return key) to trigger the button click
    players_name_entry.bind("<Return>", simulate_button_click)

    # Initialize the counter inside the button to track the number of inputs
    submit_players_name_button.counter = {'value': 0}

def add_to_players_names(entry, players_names, players_quantity, counter, update_player_label):
    # Get input text from the entry field
    input_text = entry.get()
    if input_text.strip():  # Ensure input is not empty
        # Add the text to the players_names list
        players_names.append(input_text.strip())

        # Clear the entry field after submission
        entry.delete(0, tk.END)
        entry.insert(0, ' ')

        counter['value'] += 1

        if counter['value'] < players_quantity:
            # Update the label to show the next player's number
            update_player_label(counter['value'])
        else:
            # If all names are entered, proceed to the game start
            players_timeline = [[] for _ in range(players_quantity)]
            previous_songs = [-1]
            current_player = 0
            current_round = 1
            starting_timelines(players_timeline, players_quantity, previous_songs)
            game_start(players_timeline, players_names, previous_songs, current_player, current_round, players_quantity)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Menu Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def start_sequence():    
    clear_window(root)
    
    # Create label for entry field
    players_number_label = tk.Label(root, text="Podaj liczbę graczy", font=(GUI_CSS.font_name, 24), bg=GUI_CSS.main, fg=GUI_CSS.font)
    players_number_label.pack(pady=(GUI_CSS.menu_pady,GUI_CSS.pady))

    # Create rectangular entry field for the initial number input
    players_number_entry = tk.Entry(root, font=(GUI_CSS.font_name, 20), bg=GUI_CSS.button, fg=GUI_CSS.font, justify="center")
    players_number_entry.pack(pady=GUI_CSS.pady)
    players_number_entry.focus_set()

    # Create an error label for displaying validation messages
    error_label = tk.Label(root, text="", fg="red", bg=GUI_CSS.main, font=(GUI_CSS.font_name, 12))
    error_label.pack(pady=0)

    # Create the start button
    players_number_input_button = RoundedButton(root, 
    text="DALEJ", radius=GUI_CSS.menu_button_radius, btnbackground=GUI_CSS.button, btnforeground=GUI_CSS.font, border_color=GUI_CSS.border, border_width=GUI_CSS.menu_button_border_width, buttonWidth=GUI_CSS.menu_button_width, buttonHeight=GUI_CSS.menu_button_height,
    clicked=lambda: players_number_input(players_number_entry, players_names, root, error_label))
    players_number_input_button.pack(pady=GUI_CSS.pady)
    
    # Function to simulate the button click
    def simulate_button_click(event=None):
        players_number_input_button.clicked()  # Simulates the button click
    # Bind the Enter key (Return key) to trigger the button click
    players_number_entry.bind("<Return>", simulate_button_click)

    #Game variables
    players_names=[]

def close_sequence():
    root.destroy()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Guessing View Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_players_round(number_of_buttons, players_timeline, current_round, players_names, current_player, guess_var):
    # Layout
    layout(players_names,current_player,current_round)

    # Guessing
    # Managing width and height of the buttons
    def height_of_buttons(number_of_buttons):
        if number_of_buttons <= 4:
            return 70
        return 359 // number_of_buttons
    buttonHeight = height_of_buttons(number_of_buttons)
    buttonWidth = GUI_CSS.menu_button_width

    # Create a frame to contain the buttons and labels
    button_frame = tk.Frame(root, bg=GUI_CSS.main)
    button_frame.pack(expand=True)
    
    # Lower the button_frame to the background layer
    button_frame.lower()
    
    # Create buttons and their corresponding labels
    for i in range(number_of_buttons):
        button = RoundedButton(
            button_frame,
            text=f"Pozycja {i + 1}",
            radius=GUI_CSS.menu_button_radius,
            btnbackground=GUI_CSS.button,
            btnforeground=GUI_CSS.font,
            border_color=GUI_CSS.border,
            border_width=GUI_CSS.menu_button_border_width,
            buttonWidth=buttonWidth,
            buttonHeight=buttonHeight,
            clicked=lambda i=i: guess_var.set(i + 1)  # Set the clicked button index
        )
        button.pack(pady=4)

        button_label = tk.Label(
            button_frame,
            text=f"{players_timeline[current_player][i][0]} {players_timeline[current_player][i][1]} {players_timeline[current_player][i][2]}",
            font=(GUI_CSS.font_name, int(buttonHeight * 0.3)),
            bg=GUI_CSS.main,
            fg=GUI_CSS.font
        )

        if number_of_buttons >= 8:
            button_label.pack(pady=0)
        else:
            button_label.pack(pady=2)

    # Add one extra button at the end
    button = RoundedButton(
        button_frame,
        text=f"Pozycja {number_of_buttons + 1}",
        radius=GUI_CSS.menu_button_radius,
        btnbackground=GUI_CSS.button,
        btnforeground=GUI_CSS.font,
        border_color=GUI_CSS.border,
        border_width=GUI_CSS.menu_button_border_width,
        buttonWidth=buttonWidth,
        buttonHeight=buttonHeight,
        clicked=lambda: guess_var.set(number_of_buttons + 1)
    )
    button.pack(pady=4)

def game_start(players_timeline, players_names, previous_songs, current_player, current_round, players_quantity):
    game_stopper=stop_game(players_timeline)
    while game_stopper!=True:
        round_players_timeline=current_player_timeline(players_timeline[current_player])
        
        clear_window(root)
        # Starting song button
        def start_song_view(song):
            song_started_var = tk.BooleanVar()
            song_started_var.set(False)
            def on_start_song_button_click():
                play_song(song)
                song_started_var.set(True)
            start_song_button = RoundedButton(root, text="Puść piosenkę", radius=GUI_CSS.menu_button_radius, btnbackground=GUI_CSS.button, btnforeground=GUI_CSS.font, border_color=GUI_CSS.border, border_width=GUI_CSS.menu_button_border_width, buttonWidth=330, buttonHeight=120, 
            clicked=on_start_song_button_click)
            start_song_button.pack(padx=20, pady=(340,20))
            root.wait_variable(song_started_var)
            clear_window(root)
        layout(players_names,current_player,current_round)
        year,title,author,song=random_song(previous_songs).split(';')
        while play_song_test(song)!=True:
            year,title,author,song=random_song(previous_songs).split(';')
        start_song_view(song)

        # Create and initialize Tkinter variable to store the guess
        guess_var = tk.IntVar()
        guess_var.set(0) 

        # Create Players Round
        num_buttons = len(players_timeline[current_player])
        create_players_round(num_buttons, players_timeline, current_round, players_names, current_player, guess_var)

        # Wait for the button to be clicked
        root.wait_variable(guess_var)
        guess=guess_var.get()
        guess-=1
        window_width = root.winfo_width()
        # If it was correct guess
        if is_correct_answer(round_players_timeline,guess,year)==True:
            clear_window(root)
            # Layout
            correct_answer_label = tk.Label(root, text="Prawidłowa odpowiedź", font=(GUI_CSS.font_name, 36), bg=GUI_CSS.main, fg=GUI_CSS.font)
            correct_answer_label.pack(pady=(GUI_CSS.menu_pady+70, GUI_CSS.pady))
            wrap_length = int(window_width * 0.9)
            answer_label = tk.Label(
                root, text=f"To był utwór {title} wykonany przez {author} z {year} roku",
                font=(GUI_CSS.font_name, 28), bg=GUI_CSS.main, fg=GUI_CSS.font, wraplength=wrap_length
            )
            answer_label.pack(pady=GUI_CSS.pady)

            
            # Add the song to the player's timeline
            players_timeline[current_player]=add_song(players_timeline[current_player],year,title,author)
            
            # Force update to render the labels
            root.update()

            # Pause execution for 5 seconds
            time.sleep(5) 

        # If it was not correct guess
        elif is_correct_answer(round_players_timeline,guess,year)==False:
            clear_window(root)
            # Layout
            # layout(players_names,current_player,current_round)
            wrong_answer_label = tk.Label(root, text="Zła odpowiedź", font=(GUI_CSS.font_name, 36), bg=GUI_CSS.main, fg=GUI_CSS.font)
            wrong_answer_label.pack(pady=(GUI_CSS.menu_pady+70, GUI_CSS.pady))
            wrap_length = int(window_width * 0.9)
            answer_label = tk.Label(
                root, text=f"To był utwór {title} wykonany przez {author} z {year} roku",
                font=(GUI_CSS.font_name, 28), bg=GUI_CSS.main, fg=GUI_CSS.font, wraplength=wrap_length
            )
            answer_label.pack(pady=GUI_CSS.pady)
            
            # Force update to render the labels
            root.update()

            # Pause execution for 5 seconds
            time.sleep(5) 
        
        stop_song()
        game_stopper=stop_game(players_timeline)
        if current_player+1==players_quantity:
            current_player=0
            current_round+=1
        elif current_player+1<players_quantity:
            current_player+=1
    
    clear_window(root)        
    # Layout
    end_game_label = tk.Label(root, text="Koniec gry!", font=(GUI_CSS.font_name, 36), bg=GUI_CSS.main, fg=GUI_CSS.font)
    end_game_label.pack(pady=(GUI_CSS.menu_pady+70, GUI_CSS.pady))
    winner_label = tk.Label(root, text=f"Wygrał {players_names[current_player-1]}", font=(GUI_CSS.font_name, 28), bg=GUI_CSS.main, fg=GUI_CSS.font)
    winner_label.pack(pady=GUI_CSS.pady)

def layout(players_names, current_player, current_round):
    # Create menu button in the right bottom corner
    menu_button = RoundedButton(
        root, 
        text="MENU", 
        radius=GUI_CSS.menu_button_radius, 
        btnbackground=GUI_CSS.button, 
        btnforeground=GUI_CSS.font, 
        border_color=GUI_CSS.border, 
        border_width=GUI_CSS.menu_button_border_width, 
        buttonWidth=GUI_CSS.menu_button_width, 
        buttonHeight=GUI_CSS.menu_button_height, 
        clicked=main_menu
    )
    menu_button.place(x=root.winfo_screenwidth() - 220, y=root.winfo_screenheight() - 120)

    # Create a single frame to contain all components with a border and background color
    container_frame = tk.Frame(root, bg=GUI_CSS.border, bd=GUI_CSS.menu_button_border_width)
    container_frame.place(x=5, y=5)  # Adjust the position as needed

    # Inside the frame, create a sub-frame for content with the desired background color
    content_frame = tk.Frame(container_frame, bg=GUI_CSS.button)
    content_frame.pack(padx=GUI_CSS.menu_button_border_width, pady=GUI_CSS.menu_button_border_width)

    # Add round label
    round_label = tk.Label(content_frame, text=f"Tura {current_round}", font=(GUI_CSS.font_name, 32), bg=GUI_CSS.button, fg=GUI_CSS.font)
    round_label.grid(row=0, column=0, sticky="w", padx=(5, 0), pady=5)

    # Add queue label
    queue_label = tk.Label(content_frame, text=f"Kolejka gracza:", font=(GUI_CSS.font_name, 32), bg=GUI_CSS.button, fg=GUI_CSS.font)
    queue_label.grid(row=1, column=0, sticky="w", padx=(5, 0), pady=5)

    # Add players label
    players_label = tk.Label(content_frame, text=f"{players_names[current_player]}", font=(GUI_CSS.font_name, 32), bg=GUI_CSS.button, fg=GUI_CSS.font)
    players_label.grid(row=2, column=0, sticky="w", padx=(5, 0), pady=5)

    # Function to hide the container when the mouse is over it
    def hide_container(event):
        container_frame.place_forget()  # Hide the container

    # Function to check if the mouse is outside the container and show it
    def check_mouse_position(event):
        # Get mouse coordinates
        x, y = event.x_root, event.y_root
        
        # Get the container's bounding box
        if container_frame.winfo_ismapped():  # Skip if already hidden
            return
        container_bbox = container_frame.bbox() if container_frame.winfo_ismapped() else (0, 0, 0, 0)
        
        # If the mouse is outside the container, show it
        if not (container_bbox[0] <= x <= container_bbox[2] and container_bbox[1] <= y <= container_bbox[3]):
            container_frame.place(x=5, y=5)  # Show the container
    # Bind hover events to the container_frame
    container_frame.bind("<Enter>", hide_container)  # Hide when mouse enters

    # Bind mouse movement to the root window to check position and show container
    root.bind("<Motion>", check_mouse_position)  # Track mouse movements globally


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Menu Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main_menu():
    clear_window(root)
    
    end_game_label = tk.Label(root, text="Year That Song", font=(GUI_CSS.font_name, 72), bg=GUI_CSS.main, fg=GUI_CSS.font)
    end_game_label.pack(pady=100)

    start_button = RoundedButton(root, text="START", radius=GUI_CSS.menu_button_radius, btnbackground=GUI_CSS.button, btnforeground=GUI_CSS.font, border_color=GUI_CSS.border, border_width=GUI_CSS.menu_button_border_width, buttonWidth=GUI_CSS.menu_button_width, buttonHeight=GUI_CSS.menu_button_height, clicked=start_sequence)
    start_button.pack(padx=20, pady=(10,GUI_CSS.pady+5))

    exit_button = RoundedButton(root, text="EXIT", radius=GUI_CSS.menu_button_radius, btnbackground=GUI_CSS.button, btnforeground=GUI_CSS.font, border_color=GUI_CSS.border, border_width=GUI_CSS.menu_button_border_width, buttonWidth=GUI_CSS.menu_button_width, buttonHeight=GUI_CSS.menu_button_height, clicked=close_sequence)
    exit_button.pack(padx=20, pady=GUI_CSS.pady+5)

def clear_window(root):
    for widget in root.winfo_children():
        widget.destroy()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Code~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(background=GUI_CSS.main)
main_menu()
root.mainloop()