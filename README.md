
# CasinoMines Implementation
CasinoMines implementation. Probablistic-approach for money multipliers. Mathematicall paper attached in docs/MathOfGame.ipynb.


# Video Demo
https://github.com/user-attachments/assets/d20b3373-fe8c-4f84-82d2-c6023975c602


## Algorithms & Data Structures

- Binary search and merge sort. Find their implementations in src/others/algorithms.


## Features

- Interactive GUI for playing Mines
- Probability calculations and statistical analysis
- Customizable game parameters
- Real-time win probability display


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/javidsegura/casinomines.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r docs/requirements.txt
   ```
3. Run src/main.py


## Tree

```
├── README.md                         # Project documentation
├── docs                              # Documentation and supporting files
│   ├── MathOfGame.ipynb              # Mathematical paper
│   ├── requirements.txt              # Python dependencies for the project
│   └── tree.txt                      # Directory structure
├── src                               # Source code for the project
│   ├── board                         # Board-related modules
│   │   ├── grid.py                   # Handles grid logic
│   │   ├── header.py                 # Header layout and management
│   │   ├── mines.py                  # Mines placement logic
│   │   └── settings.py               # Game board settings
│   ├── design                        # Design-related modules
│   │   └── game_css.py               # CSS and design configurations
│   ├── game_tabs                     # UI and tab-related logic
│   │   ├── data.py                   # Data tab implementation
│   │   ├── game_stats_ui.py          # UI for game statistics
│   │   ├── leaderboard_ui.py         # UI for leaderboard
│   │   └── payout.py                 # Handles payout calculations
│   ├── main.py                       # Entry point for the application
│   └── others                        # Miscellaneous modules
│       ├── algorithms                # Algorithms used in the game
│       │   ├── searching.py          # Searching algorithm implementations
│       │   └── sorting.py            # Sorting algorithm implementations
│       ├── confetty.py               # Confetti effect implementation
│       ├── login_dialog.py           # Handles login dialog logic
│       ├── multiplier.py             # Multiplier logic
│       ├── simulateGame.py           # Game simulation logic
│       ├── sound_effects.py          # Sound effects handling
│       └── wallet.py                 # Wallet management
└── utils                             # Utility files
    ├── data                          # Data-related assets
    │   ├── game_stats.csv            # Game statistics data
    │   └── leaderboard.csv           # Leaderboard data
    ├── fonts                         # Font files
    │   └── ZenDots-Regular.ttf       # Font used in the project
    ├── imgs                          # Image assets
    │   ├── canvas.png                # Canvas image
    │   ├── cells                     # Cell-related images
    │   │   ├── bomb.png              # Bomb icon
    │   │   ├── coin.png              # Coin icon
    │   │   └── diamond.png           # Diamond icon
    │   ├── dollar.png                # Dollar icon
    │   ├── gambling_icon.png         # Gambling-themed icon
    │   ├── horizontalDecoration.png # Horizontal decoration image
    │   ├── log_in.png                # Login icon
    │   └── podium.png                # Podium icon
    └── sound_effects                 # Sound effects
        ├── click.wav                 # Click sound effect
        ├── error.wav                 # Error sound effect
        └── win.wav                   # Winning sound effect

```