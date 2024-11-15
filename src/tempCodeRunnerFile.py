class CasinoMines(QWidget, GameStyle):
    """ Controls the main window of the game"""
    def __init__(self) -> None:
        super().__init__()

        # vars for game components
        self.minesClass = MinesLogic()
        self.gridClass = GridLogic(self.on_cell_click) 
        self.settingsClass = Settings()
        self.sound_effectsClass = SoundEffects()
        # vars for game stats
        self.game_in_progress = False
        self.clicked_cells = set()
        # vars for csvs
        self.gamesPlayed = 0
        self.bombHit = False
        self.username = None
        
        # Set up the main UI window
        self.setWindowTitle("CasinoMines Game")
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet(GameStyle().get_stylesheet())

        # Create the main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Setup the header
        self.main_layout.addWidget(self.settingsClass.header_element())

        # Create a container widget for the game content 
        self.game_container = QWidget()
        self.game_layout = QHBoxLayout(self.game_container)
        self.game_layout.setSpacing(20)

        # Setup the configuration panel
        left_layout = self.configuration_panel()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.game_layout.addWidget(left_widget, 1)

        # Setup the game grid
        grid_widget = QWidget()
        grid_widget.setLayout(self.gridClass.setup_grid())
        grid_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.game_layout.addWidget(grid_widget, 2)
        self.gridClass.disable_grid(True)  # Initially disable the grid

        # Game tabs
        self.user_data = UserData()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.game_container, "CasinoMines Game")
        self.data_tab = DataTab()
        self.tabs.addTab(self.data_tab, "Game Data")
        self.leaderboard = LeaderBoardTab(self.user_data)
        self.tabs.addTab(self.leaderboard, "Leaderboard") 
        self.leaderboard.populateRanking()

        # Payout tab