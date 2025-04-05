# Hitster

Hitster is a personal project designed to showcase the fundamentals of **Python** programming and **Spotify API** integration. This project demonstrates the creation of a music-based game where players guess the correct timeline of songs, featuring two versions: a **Command-Line Interface (CLI)** and a **Graphical User Interface (GUI)**.

---

## 🚀 Features

- **Spotify Integration**: Fetches song data and plays tracks directly from Spotify.
- **Two Game Modes**: Play using a CLI or an interactive GUI.
- **Dynamic Gameplay**: Randomized song selection ensures unique experiences every time.
- **Multiplayer Support**: Allows multiple players to compete in guessing the correct song timeline.
- **Customizable Settings**: Easily adjust the number of songs required to win.
- **Personal Playlist Support**: Easily add your own Spotify playlists to customize the game experience.

---

## 📂 Project Structure

Hitster/
│
├── CLI_game.py # Command-line version of the game
├── GUI_game.py # Graphical version of the game
├── GUI_CSS.py # Styling for the GUI
├── game_functions.py # Core game logic and functions
├── song_player.py # Handles Spotify playback
├── song_randomizer.py # Randomizes song selection
├── database_updater.py # Updates the song database using Spotify API
├── internet_test.py # Tests internet connectivity and Spotify API
├── spotify_credentials.py # Spotify API credentials and settings
├── MusicFiles/ # Contains song data files
│ └── dane.txt
│
├── screenshots/ # Screenshots of the game
├── README.md # Project documentation
├── LICENSE # License file
└── .gitignore # Git ignore file

---

## 🛠️ Technologies Used

- **Python**: Core programming language for the project.
- **Spotipy**: Python library for Spotify Web API integration.
- **Tkinter**: For creating the graphical user interface.
- **Spotify API**: For fetching song data and playback.
- **Random**: For randomizing song selection.

---

## 🌟 Key Functionalities

1. **CLI Mode**:

   - Players take turns guessing the correct position of songs in their timeline.
   - Songs are played directly from Spotify.

2. **GUI Mode**:

   - Interactive interface with buttons and labels for a seamless experience.
   - Dynamic song playback and timeline updates.

3. **Database Management**:

   - Fetches and updates song data from Spotify playlists.
   - Stores song information in text files for offline use.

4. **Multiplayer Gameplay**:
   - Supports multiple players with individual timelines.
   - Tracks progress and determines the winner.

---

## 📸 Screenshots

### Command Line Version

#### Main Menu

![Main Menu](screenshots/CLI_Welcome_Page.png.png)

#### Gameplay

![Gameplay](screenshots/Gameplay.png)

### End Screen

![End Screen](screenshots/EndScreen.png)

---

## ⚙️ Installation and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/Hitster
   ```

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is under the MIT License - see the [LICENSE](./LICENSE) file for details.
