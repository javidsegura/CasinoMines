""" Controls the flow of the game. Start game running this file"""

from design.game_css import GameStyle
from board.mines import MinesLogic
from board.grid import GridLogic
from board.settings import Settings
from others.sound_effects import SoundEffects
from game_tabs.data import UserData
from game_tabs.game_stats_ui import DataTab
from game_tabs.payout import PayoutTab
from game_tabs.leaderboard_ui import LeaderBoardTab
from others.login_dialog import show_login_dialog
from others.confetty import ConfettiEffect
import sys

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QSizePolicy, QMessageBox, QTabWidget)
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

    
class CasinoMines(QWidget, GameStyle):
    """ Controls the main window of the game"""
    def __init__(self) -> None:
        """
        Time Complexity: O(1)
        """
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
        self.payout_tab = PayoutTab(self.settingsClass)
        self.tabs.addTab(self.payout_tab, "Payout")


        # Add the game container to the main layout
        self.main_layout.addWidget(self.tabs)

        # Show the window and get the username
        self.show()
        self.confetti = ConfettiEffect(self)
        self.confetti.resize(self.size())
        self.confetti.hide() # Activate confetti but down show yet
        self.username = self.show_userPopup()
        self.leaderboard.defineUsername(self.username)

    def start_game(self) -> None:
        """ 
        Description: Function executed when the user clicks on the start
        Time Complexity: 
            Avg Case: O(n)
            Worst Case: O(n^2)
        Inner Functions:
            get_num_mines: O(1)
            reset_for_new_game: O(1)
            create_mineField: O(n) or  O(n^2) 
            disable_cash_out_button: O(1)
        """
        self.num_mines = self.settingsClass.get_num_mines()
        self.game_in_progress = True 
        self.gamesPlayed += 1
        self.settingsClass.reset_for_new_game()
        self.clicked_cells.clear()
        self.create_minefield()
        self.start_button.setDisabled(True) 
        self.gridClass.disable_grid(False) 
        self.settingsClass.disable_cash_out_button()
        self.num_mines = self.settingsClass.get_num_mines()

    def create_minefield(self) -> None:
        """
        Description: Create set of mines in the grid
        Time Complexity: 
            Avg Case: O(n)
            Worst Case: O(n^2)
        Inner Functions:
            reset_buttons: O(n)
            get_mines_set: O(n) or  O(n^2) 
        """
        self.gridClass.reset_buttons() # Reset the grid
        self.minesClass.get_mines_set(self.num_mines) # Create set of mines
   
    def on_cell_click(self, row:int, col:int) -> None:
        """
        Description: Function executed when the user clicks on a cell
        Time Complexity: O(n * m)
        Inner Functions:
            is_mine: O(1)
            play_lose: O(1)
            game_over: O(n * m)
            play_click: O(1)
            disable_button: O(1)
            update_multiplier: O(n)
            update_profit: O(1)
            activate_cash_out_button: O(1)
            increase_cash_out_button: O(1)
        """
        if not self.game_in_progress:
            raise Exception("Game is not in progress. You cannot click on cells")
        self.clicked_cells.add((row, col))

        # If clicked cell is a mine
        if self.minesClass.is_mine(row, col):
            self.gridClass.set_button_state(row, col,True, revealed=False)
            self.bombHit = True
            self.sound_effectsClass.play_lose()
            self.game_over()
        else: 
            self.sound_effectsClass.play_click()
            self.gridClass.set_button_state(row, col, False, revealed=False)
            self.bombHit = False
            self.gridClass.disable_button(row, col)
            self.settingsClass.update_multiplier(len(self.clicked_cells)-1)
            self.settingsClass.update_profit()

            if len(self.clicked_cells) > 0:
                self.settingsClass.activate_cash_out_button()
                self.settingsClass.increase_cash_out_button()
            
            self.settingsClass.update_multiplier(len(self.clicked_cells)-1)
            self.settingsClass.update_profit()

            if len(self.clicked_cells) > 0:
                self.settingsClass.activate_cash_out_button()
                self.settingsClass.increase_cash_out_button()
    
    def configuration_panel(self) -> QVBoxLayout:
        """ 
        Description: Defines left-most menu. 
        Time Complexity: O(1)
        Inner Functions:
            set_start_button: O(1)
        """
        left_layout, self.cash_out_button = self.settingsClass.set_up_panel()
        self.cash_out_button.clicked.connect(self.handle_cash_out)

        # Start button is added from here to avoid circular import
        self.start_button = QPushButton("Start Game")
        self.start_button.setObjectName("startButton")
        self.start_button.clicked.connect(self.start_game)
        self.start_button.setDisabled(True)
        left_layout.addWidget(self.start_button)
        self.settingsClass.set_start_button(self.start_button)

        return left_layout

    def handle_cash_out(self) -> None:
        """ 
        Description: Controls what happens when the user clicks on the cash out button
        Time Complexity: O(n * m)
        Inner Functions:
            add_user_data: O(n * m)
            reveal_cells: O(n)
            show_CashOut_screen: O(1)
            cash_out: O(1)
        """
        self.add_user_data(win=True)
        if self.game_in_progress and len(self.clicked_cells) > 0:
            self.gridClass.reveal_cells(self.minesClass.set_of_mines(), self.clicked_cells)
            self.show_CashOut_screen()
            self.settingsClass.cash_out()
            self.game_in_progress = False
            
    def game_over(self) -> None:
        """ 
        Description: Defines behavior after user clicked on a cell with a mine
        Time Complexity: O(n * m)
        Inner Functions:
            add_user_data: O(n * m)
            reveal_cells: O(n)
            show_Gameover_screen: O(1)
        """
        self.game_in_progress = False
        if self.bombHit:
            self.add_user_data(win=False)
            self.gridClass.reveal_cells(self.minesClass.set_of_mines(), self.clicked_cells)
            self.show_GameOver_screen()

    def show_CashOut_screen(self) -> None:
        """ 
        Description: Shows a game over pop-up and resets the game when dismissed 
        Time Complexity: O(1)
        """
        self.confetti.resize(self.size())
        self.confetti.raise_()
        self.confetti.start_animation()
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("You win!")
        self.sound_effectsClass.play_win() 

        # Create a custom layout for the message box
        layout = QVBoxLayout()
        multiplier_label = QLabel(f"x{self.settingsClass.get_prior_multiplier()}")
        multiplier_label.setAlignment(Qt.AlignCenter)
        multiplier_label.setStyleSheet("font-size: 78px; font-weight: bold; margin-bottom: 10px; color: #ffcc00;")
        layout.addWidget(multiplier_label)

        # Add text with the money won
        profit_label = QLabel(f"You Won <span style='color: #ffcc00;'>${self.settingsClass.get_prior_profit():.2f}</span>")
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

    def reset_game_after_cash_out(self) -> None:
        """ 
        Description: Resets the game after cashing out 
        Time Complexity: O(n) 
        Inner Functions:
            activate_btns: O(n)
            reset_bet: O(1)
            reset_buttons: O(n)
            reset_for_new_game: O(1)
            disable_cash_out_button: O(1)
            disable_cash_out_button: (1)
        """
        self.game_in_progress = False
        self.start_button.setDisabled(True)
        self.gridClass.disable_grid(True)
        self.settingsClass.activate_btns()
        self.settingsClass.reset_bet()
        self.gridClass.reset_buttons()
        self.settingsClass.reset_for_new_game()
        self.settingsClass.disable_cash_out_button()

    def show_GameOver_screen(self) -> None:
        """  
        Description: Shows a game over pop-up and resets the game when dismissed
        Time Complexity: O(1)
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("You clicked on a bomb!")

        # Create a custom layout for the message box
        layout = QVBoxLayout()
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

    def reset_game_after_gameover(self) -> None:
        """ Resets the game after the pop-up is dismissed """
        self.settingsClass.activate_btns()
        self.settingsClass.reset_bet()
        self.game_in_progress = False
        self.gridClass.reset_buttons()
        self.settingsClass.reset_for_new_game()
        self.start_button.setDisabled(True)
        self.gridClass.disable_grid(True)
        self.settingsClass.disable_cash_out_button()
        self.settingsClass.restart_cash_out_button()
    
    def show_userPopup(self) -> str:
        """ 
        Description: Defines log in element popup
        Time Complexity: O(1)
        Inner Functions:
            show_login_dialog: Generally O(1)
            defineUsername: O(1)
        """
        username = show_login_dialog(self)
        self.settingsClass.defineUsername(username)
        return username

    def returnUser(self) -> str:
        """
        Time Complexity: O(1)
        """
        return self.username

    def calcProfit(self) -> float:
        """
        Time Complexity: O(1)
        Inner Functions:
            getBet: O(1)
            getProfit: O(1)
        """
        if self.bombHit:
            return - self.settingsClass.getBet()
        else:
            return self.settingsClass.getProfit()

    def add_user_data(self, win:bool) -> None:
        """
        Description:  Update databases with user data
        Time Complexity: O(n * m), where n and m are the dimensions relevant to the operations inside populateGameStats()
        Inner Functions:
            calcProfit: O(1)
            add_user_data: O(n)
            populateGameStats: O(n * m)
            add_leaderboard_data: O(nlogn)
            populateRanking: O(n)
        """
        profit = self.calcProfit()

        self.user_data.add_user_data(win=win, game_id=self.gamesPlayed, bet=self.settingsClass.getBet(),
                                      mines=self.settingsClass.getBombs(), balanceBefore=self.settingsClass.getBalanceBeforeChange(), 
                                      balanceAfter=self.settingsClass.getBalanceBeforeChange() + profit, profit=profit)
        self.data_tab.populateGameStats()

        self.user_data.add_leaderboard_data(user=self.username, balance=self.settingsClass.getBalanceBeforeChange() + profit)
        self.leaderboard.populateRanking() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CasinoMines()
    sys.exit(app.exec())