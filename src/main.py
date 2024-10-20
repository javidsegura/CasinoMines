"""
This module should serve as a general control of the GUI.

It should mainly be reduced to function calls to other modules.

"""

import sys,os, json

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame, QMessageBox, QTabWidget)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget


from game_css import GameStyle
from bombs import BombsLogic
from grid import GridLogic
from wallet import Wallet
from configuration_panel import ConfigurationPanel
from header import Header
from data import UserData
from sound_effects import SoundEffects
from data_tab import DataTab

    

class CasinoMines(QWidget, GameStyle):
    """ Controls the main window of the game"""
    def __init__(self):
        super().__init__()
        self.grid_size = 5
        self.bombs_logic = BombsLogic(self.grid_size)
        self.grid_logic = GridLogic(self.grid_size, self.on_cell_click) #call data.py after this for profit
        self.config_panel = ConfigurationPanel()
        self.wallet = Wallet()
        self.header = Header()
        self.sound_effects = SoundEffects()
        self.game_in_progress = False
        self.clicked_cells = set()
        self.cells_clicked = 0 # is this not redudant?
        # variables for data
        self.gamesPlayed = 0
        self.bombHit = False

    
        
        # Set up the main UI window
        self.setWindowTitle("CasinoMines Game")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(GameStyle().get_stylesheet())

        # Create the main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Setup the header
        self.main_layout.addWidget(self.config_panel.header_element())

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
        grid_widget.setLayout(self.grid_logic.setup_grid())
        grid_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.game_layout.addWidget(grid_widget, 2)


        # Data Tab
        self.tabs = QTabWidget()
        self.tabs.addTab(self.game_container, "CasinoMines Game")

        self.data_tab = DataTab()
        # self.data_layout = QVBoxLayout()
        # self.data_label = QLabel("Game Data")
        # self.data_layout.addWidget(self.data_label)
        # self.data_tab.setLayout(self.data_layout)

        self.tabs.addTab(self.data_tab, "Game Data")

        self.user_data = UserData()
        self.user_data.initialize_csv()

        # Add the game container to the main layout
        self.main_layout.addWidget(self.tabs)

        self.grid_logic.disable_grid(True)  # Initially disable the grid
        self.show()

    def configuration_panel(self):
        """ Defines left-most menu. """
        left_layout, self.cash_out_button = self.config_panel.set_up_panel()
        self.cash_out_button.clicked.connect(self.handle_cash_out)

        # Start button is added from here to avoid circular import
        self.start_button = QPushButton("Start Game")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setDisabled(True)
        left_layout.addWidget(self.start_button)
        self.config_panel.set_start_button(self.start_button)

        return left_layout

    def start_game(self):
        """Function executed when the user clicks on the start button"""
        self.gamesPlayed += 1
        print(f"\n\n\033[1mGame {self.gamesPlayed}:\033[0m\n")

        self.num_mines = self.config_panel.get_num_mines()
        self.create_minefield()
        self.start_button.setDisabled(True) # Disable start button
        self.grid_logic.disable_grid(False) # Activate the grid
        self.game_in_progress = True # Game is in progress
        self.cells_clicked = 0
        #self.clicked_cells.clear()
        self.config_panel.reset_for_new_game()
        self.config_panel.disable_cash_out_button()

    def create_minefield(self) -> None:
        """Create set of mines in the grid"""
        self.grid_logic.reset_buttons() # Reset the grid
        self.bombs_logic.get_mines_set(self.num_mines) # Create set of mines
   
    def on_cell_click(self, row:int, col:int) -> None:
        """Function executed when the user clicks on a cell"""
        if not self.game_in_progress:
            return
        self.clicked_cells.add((row, col))
        self.cells_clicked += 1
        if self.bombs_logic.is_mine(row, col):
            self.grid_logic.set_button_state(row, col,True, revealed=False)
            self.bombHit = True
            self.sound_effects.play_lose()
            self.game_over()
        else:
            self.sound_effects.play_click()
            self.grid_logic.set_button_state(row, col, False, revealed=False)
            self.bombHit = False
            self.grid_logic.disable_button(row, col)
            self.config_panel.update_multiplier()
            self.config_panel.update_profit()

            if self.cells_clicked >= 1:
                self.config_panel.activate_cash_out_button()
                self.config_panel.increase_cash_out_button()
            
            self.config_panel.update_multiplier()
            self.config_panel.update_profit()

            if self.cells_clicked >= 1:
                self.config_panel.activate_cash_out_button()
                self.config_panel.increase_cash_out_button()
            
    def game_over(self):
        """ Defines behavior after user clicked on a cell with a mine"""
        # adding userData to csv if bomb clicked
        self.add_user_data()

        self.game_in_progress = False

        # Reveling unclicked cells
        self.grid_logic.reveal_cells(self.bombs_logic.set_of_mines(), self.clicked_cells)

        # Deactivate corresponding widgets of the GUI
        self.grid_logic.disable_grid(True)
        self.show_GameOver_screen()
    
    def handle_cash_out(self):
        """ Controls what happens when the user clicks on the cash out button"""
        self.add_user_data()

        if self.game_in_progress and self.cells_clicked > 0:
            self.grid_logic.reveal_cells(self.bombs_logic.set_of_mines(), self.clicked_cells)
            self.show_CashOut_screen()
            self.config_panel.cash_out()

    def show_CashOut_screen(self):
        """ Shows a game over pop-up and resets the game when dismissed """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("You win!")

        self.sound_effects.play_win() 

        # Create a custom layout for the message box
        layout = QVBoxLayout()

        # Add a large title with the multiplier
        multiplier_label = QLabel(f"x{self.config_panel.get_prior_multiplier()}")
        
        multiplier_label.setAlignment(Qt.AlignCenter)
        multiplier_label.setStyleSheet("font-size: 78px; font-weight: bold; margin-bottom: 10px; color: #ffcc00;")
        layout.addWidget(multiplier_label)

        # Add text with the money won
        profit_label = QLabel(f"You Won <span style='color: #ffcc00;'>${self.config_panel.get_prior_profit():.2f}</span>")
        profit_label.setAlignment(Qt.AlignCenter)
        profit_label.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
        layout.addWidget(profit_label)

        # Set the custom layout to the message box
        msg_box.layout().addLayout(layout, 0, 0, 1, msg_box.layout().columnCount())

        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setText("Play again")

        # Connect the buttonClicked signal to our reset function
        msg_box.buttonClicked.connect(self.reset_game_after_cash_out)
        msg_box.exec()

    def reset_game_after_cash_out(self):
        """ Resets the game after cashing out """
        self.config_panel.activate_btns()
        self.config_panel.reset_bet()
        self.game_in_progress = False
        self.cells_clicked = 0
        self.clicked_cells.clear()
        self.grid_logic.reset_buttons()
        self.config_panel.reset_for_new_game()
        self.start_button.setDisabled(True)
        self.grid_logic.disable_grid(True)
        self.config_panel.disable_cash_out_button()


    def show_GameOver_screen(self):
        """ Shows a game over pop-up and resets the game when dismissed """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("You clicked on a bomb!")

        # Create a custom layout for the message box
        layout = QVBoxLayout()

        # Add a large title with the multiplier
        multiplier_label = QLabel(f"BOMB!")
        
        multiplier_label.setAlignment(Qt.AlignCenter)
        multiplier_label.setStyleSheet("font-size: 78px; font-weight: bold; margin-bottom: 10px; color: red;")
        layout.addWidget(multiplier_label)

        # Set the custom layout to the message box
        msg_box.layout().addLayout(layout, 0, 0, 1, msg_box.layout().columnCount())

        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.button(QMessageBox.Ok).setText("Play again")

        # Connect the buttonClicked signal to our reset function
        msg_box.buttonClicked.connect(self.reset_game_after_gameover)
        msg_box.exec()


    def reset_game_after_gameover(self):
        """ Resets the game after the pop-up is dismissed """
        self.config_panel.activate_btns()
        self.config_panel.reset_bet()
        self.wallet.reset_bet()
        self.game_in_progress = False
        self.cells_clicked = 0
        self.clicked_cells.clear()
        self.grid_logic.reset_buttons()
        self.config_panel.reset_for_new_game()
        self.start_button.setDisabled(True)
        self.grid_logic.disable_grid(True)
        self.config_panel.disable_cash_out_button()
        self.config_panel.restart_cash_out_button()

    def calcProfit(self):
        if self.bombHit:
            return - self.config_panel.getBet()
        else:
            return self.config_panel.getProfit()

    # returning bet and mines for data.py
    def add_user_data(self):
        self.user_data.add_user_data(self.gamesPlayed, self.config_panel.getBet(), self.config_panel.getBombs(), self.config_panel.getBalanceBeforeChange(), self.calcProfit(), self.config_panel.getBalanceBeforeChange() + self.calcProfit())
        self.data_tab.populateValues()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CasinoMines()
    sys.exit(app.exec())
