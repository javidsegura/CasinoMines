""" 
Contains functions for the settings and the header elements
"""
import others.wallet as wallet 
import board.header as header
import others.multiplier as multiplier

from PySide6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap 


class Settings():
    """ Controls the settings panel of the game. 
    All wallet elements's value in the header are also controlled here"""
    def __init__(self) -> None:
        """
        Description: initializes the Settings class
        Time Complexity:
            - O(1): All operations run in constant time
        """
        super().__init__()
        self.setup_layout = QVBoxLayout()
        self.wallet = wallet.Wallet()
        self.header = header.Header()
        
        self.num_mines = 1
        self.start_button = None
        self.cash_out_button = None

        # vars for csv
        self.betAmount = -1
        self.numMines = -1
        self.profit = 0
        self.balanceBeforeChange = -1
    
    def defineUsername(self, username:str) -> None:
        """
        Description: defines the username
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.header.update_user(username)

    def set_up_panel(self) -> tuple[QVBoxLayout, QPushButton]:
        self.bet_panel()
        self.mines_panel()
        self.cash_out_btn()
        self.confirm_btn()
        
        # Add spacing
        self.setup_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Add spacing below button
        self.setup_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        # Add control layout to main layout (on the left)
        return self.setup_layout, self.cash_out_button
    
    def header_element(self) -> None:
        """
        Description: sets up the header element
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.header.setup_header()

    def bet_panel(self) -> None:
        """
        Description: sets up the bet panel
        Time Complexity:
            - O(n): where n is the number of percentage buttons. Note: this is asymptotically growth, and ignores the fact 
            that the number of percentage buttons is constant. The iteration through an array is however, 0(n), thus the 
            overall time complexity is O(n)
        """
        self.bet_label = QLabel("Bet Amount: ") # text label
        self.setup_layout.addWidget(self.bet_label)

        bet_input_layout = QHBoxLayout()

        dollar_sign = QLabel()
        dollar_pixmap = QPixmap("./utils/imgs/dollar.png")  
        scaled_pixmap = dollar_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        dollar_sign.setPixmap(scaled_pixmap)
        dollar_sign.setFixedSize(30, 30)  # Adjust size as needed

        bet_input_layout.addWidget(dollar_sign)

        self.bet_input = QLineEdit() # write label
        bet_input_layout.addWidget(self.bet_input)

        bet_input_layout.setStretchFactor(dollar_sign, 1)
        bet_input_layout.setStretchFactor(self.bet_input, 3)

        self.setup_layout.addLayout(bet_input_layout)

        # Percentage buttons
        self.bet_percentage_layout = QHBoxLayout()
        self.percentages_btns = []
        percentages = [10, 25, 50, 75, 100]
        for percentage in percentages:
            btn = QPushButton(f"{percentage}%")
            self.percentages_btns.append(btn)
            btn.clicked.connect(lambda _, p=percentage: self.set_bet_percentage(p))
            self.bet_percentage_layout.addWidget(btn) # Add percentage buttons to the layout
        self.setup_layout.addLayout(self.bet_percentage_layout) # Add to the whole layout


    def set_bet_percentage(self, percentage : int) -> None:
        """
        Description: computes the bet amount after clicking on percentage buttons
        Time Complexity:
            - O(1): All operations run in constant time
        """
        bet_amount = int(self.wallet.calculate_percentage_bet(percentage))
        self.bet_input.setText(f"{bet_amount}")

    def mines_panel(self) -> None:
        """
        Description: sets up the mines panel
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.mines_label = QLabel("Number of Mines: 1")
        self.setup_layout.addWidget(self.mines_label)
        self.mines_slider = QSlider(Qt.Horizontal)
        self.mines_slider.setMinimum(1)
        self.mines_slider.setMaximum(24)
        self.mines_slider.setValue(1)
        self.mines_slider.valueChanged.connect(self.update_mines_label)
        self.setup_layout.addWidget(self.mines_slider)

    def update_mines_label(self) -> None:
        """ 
        Description: updates the label of the number of mines by reading the slider value
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.mines_label.setText(f"Number of Mines: {self.mines_slider.value()}")
    
    def confirm_btn(self) -> None:
        """
        Description: sets up the confirm button
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.setup_layout.addWidget(self.confirm_button)
        # Initial state: gold color to indicate it's the next step
        self.confirm_button.setStyleSheet("background-color: #ffcc00; color: #f6f6f6; \
                                          font-weight: bold; border: 1px solid #c1cdcd; border-radius: 5px;")

        # Confirmation message
        self.confirmation_label = QLabel("")
        self.setup_layout.addWidget(self.confirmation_label)

    def confirm_selection(self) -> None:
        """
        Description: confirms the set-up of the game and enables the start button
        Time Complexity:
            - O(1): All operations run in constant time
        """
        try:
            bet_amount = int(self.bet_input.text())
            self.num_mines = self.mines_slider.value()
            self.balanceBeforeChange = self.wallet.get_balance()

            if self.num_mines < 1 or self.num_mines > 24:
                raise ValueError("Invalid number of mines. Try again!")

            if bet_amount > self.wallet.get_balance():
                raise ValueError("Bet amount exceeds wallet balance. Try again!")

            if bet_amount <= 0:
                raise ValueError("Bet amount must be greater than 0!")  

            # Initialize the multiplier function based on the game settings
            self.multiplier_func = multiplier.MultiplierFunc(25, self.num_mines)

            # Deactivate all buttons except the Start Game button
            self.deactivate_btns()
            self.wallet.place_bet(bet_amount)
            self.header.update_balance(self.wallet.get_balance())

            self.betAmount = bet_amount
            self.numMines = self.num_mines

            # Change Confirm Selection button to purple after clicking
            self.confirm_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd;\
                                               border: 1px solid #c1cdcd; border-radius: 5px;")

            # Enable the Start Game button as the next step
            if self.start_button:
                self.start_button.setDisabled(False)
                self.start_button.setStyleSheet("background-color: #ffcc00; color: #f6f6f6;\
                                                 font-weight: bold; border: 1px solid #c1cdcd; border-radius: 5px;")

        except ValueError as e:
            if str(e).startswith("invalid literal"):
                e = "You need to specify an amount to bet"
            self.show_confirmation(str(e))

    
    def show_confirmation(self, message :str) -> None:
        """
        Description: prints message on confirmation label
        Time Complexity:
            - O(1): All operations run in constant time
        """
        if message.strip().split()[:2] == ["Invalid", "literal"]:
            message = "Provide an amount to bet"
        self.confirmation_label.setText(message)
        self.confirmation_label.setStyleSheet("color: red; font-size: 18px;")
        QTimer.singleShot(3000, lambda: self.confirmation_label.setText("")) # Warning is cleared after 3 seconds

    def update_multiplier(self,index:int) -> None:
        """
        Description: updates the multiplier
        Time Complexity:
            - O(n): because of the get_next_multiplier method
        """
        try:
            new_multiplier = self.multiplier_func.get_next_multiplier(index)
            self.wallet.update_multiplier(new_multiplier)
            self.header.update_multiplier(new_multiplier)
        except Exception as e:
            print(f"Error updating multiplier: {e}")

    def get_num_mines(self) -> int:
        """
        Description: returns the number of mines in the game
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.num_mines
    
    def cash_out_btn(self) -> None:
        """
        Description: sets up the cash out button
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button = QPushButton("Cash Out")
        self.cash_out_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                                           border: 1px solid #c1cdcd; border-radius: 5px;")  # Initially purple with gold text and border
        self.cash_out_button.clicked.connect(self.cash_out)
        self.setup_layout.addWidget(self.cash_out_button)
        self.cash_out_button.setDisabled(True)  # Disable initially
        
    def reset_for_new_game(self) -> None:
        """
        Description: resets the header for a new game and prepares the buttons
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button.setDisabled(True)
        self.header.update_profit(0)
        self.header.update_multiplier(1)

        # Reset start button to purple and disable it
        if self.start_button:
            self.start_button.setDisabled(True)
            self.start_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd;\
                                             border: 1px solid #c1cdcd; border-radius: 5px;")

    def activate_cash_out_button(self) -> None:
        """
        Description: enables the cash out button
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button.setDisabled(False)

    def increase_cash_out_button(self) -> None:
        """
        Description: increases the cash out button
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button.setText(f"Cash Out: {round(self.wallet.calculate_profit() + self.wallet.get_current_bet(),2)}$")
        self.cash_out_button.setStyleSheet("background-color: #ffcc00; color: #fffce3;")
    
    def cash_out(self) -> None:
        """
        Description: cash out the current bet and show in header
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.wallet.cash_out()
        self.header.update_balance(self.wallet.get_balance())
        self.restart_cash_out_button()

    def reset_bet(self) -> None:
        """
        Description: resets the multiplier, bet and profit to intiial value in the label
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.wallet.reset_bet()
        self.header.update_profit(0)
        self.header.update_multiplier(1)

    def deactivate_btns(self) -> None:
        """
        Description: deactivates all buttons and sets them to purple to indicate inactivity
        Time Complexity:
            - O(n): where n is the number of percentage buttons. Note: this is asymptotically growth, and ignores the fact 
            that the number of percentage buttons is constant. The iteration through an array is however, 0(n), thus the 
            overall time complexity is O(n)
        """
        self.bet_input.setDisabled(True)
        self.mines_slider.setDisabled(True)
        
        # Confirm button in "disabled" state (purple)
        self.confirm_button.setDisabled(True)
        self.confirm_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                                           border: 1px solid #c1cdcd; border-radius: 5px;")
        
        # Percentage buttons in "disabled" state (purple)
        for btn in self.percentages_btns:
            btn.setDisabled(True)
            btn.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                               border: 1px solid #c1cdcd; border-radius: 5px;")
        
        # Cash Out button in "disabled" state (purple)
        self.cash_out_button.setDisabled(True)
        self.cash_out_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                                           border: 1px solid #c1cdcd; border-radius: 5px;")

    def activate_btns(self) -> None:
        """
        Description: activates all buttons and sets them appropriately based on their purpose
        Time Complexity:
            - O(n): where n is the number of percentage buttons. Note: this is asymptotically growth, and ignores the fact 
            that the number of percentage buttons is constant. The iteration through an array is however, 0(n), thus the 
            overall time complexity is O(n)
        """
        self.bet_input.setDisabled(False)
        self.mines_slider.setDisabled(False)
        
        # Confirm button in "active" state (gold)
        self.confirm_button.setDisabled(False)
        self.confirm_button.setStyleSheet("background-color: #ffcc00; color: #f6f6f6; font-weight: bold; \
                                          border: 1px solid #c1cdcd; border-radius: 5px;")

        # Percentage buttons in "inactive" state (purple)
        for btn in self.percentages_btns:
            btn.setDisabled(False)
            btn.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                              border: 1px solid #c1cdcd; border-radius: 5px;")
        
        # Cash Out button remains disabled (purple) until game progress
        self.cash_out_button.setDisabled(True)
        self.cash_out_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd;\
                                            border: 1px solid #c1cdcd; border-radius: 5px;")

        # Reset start button back to purple after it is used to start a game
        if self.start_button:
            self.start_button.setDisabled(True)
            self.start_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd;\
                                             border: 1px solid #c1cdcd; border-radius: 5px;")
    
    def update_profit(self) -> None:
        """
        Description: updates the profit label
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.header.update_profit(self.wallet.calculate_profit())
        self.profit = self.wallet.calculate_profit()

    def set_start_button(self, button: QPushButton) -> None:
        """
        Description: sets the start button reference
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.start_button = button
        # Set the initial style to purple and disable it
        self.start_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                                        border: 1px solid #c1cdcd; border-radius: 5px;")  # Purple with gold text and border
        self.start_button.setDisabled(True)

    def disable_cash_out_button(self) -> None:
        """
        Description: disables the cash out button and sets it to purple
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button.setDisabled(True)
        self.cash_out_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                                           border: 1px solid #c1cdcd; border-radius: 5px;")  # Purple with gold text

    def enable_cash_out_button(self) -> None:
        """
        Description: enables the cash out button and sets it to gold
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button.setDisabled(False)
        self.cash_out_button.setStyleSheet("background-color: #ffcc00; color: #f6f6f6; font-weight: bold; \
                                           border: 1px solid #c1cdcd; border-radius: 5px;")  # Gold with black text

    def restart_cash_out_button(self) -> None:
        """
        Description: resets the cash out button to its initial purple state
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.cash_out_button.setDisabled(True)  # Initially disabled
        self.cash_out_button.setText("Cash Out")
        self.cash_out_button.setStyleSheet("background-color: #1a0033; color: #c1cdcd; \
                                           border: 1px solid #c1cdcd; border-radius: 5px;")  # Purple with gold text

    def get_prior_profit(self) -> float:
        """
        Description: gets the profit
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.wallet.prior_profit
    
    def get_prior_multiplier(self) -> float:
        """
        Description: gets the multiplier
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.wallet.prior_multiplier
    
    def getBet(self) -> int:
        """
        Description: gets the bet
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.betAmount
    
    def getBombs(self) -> int:
        """
        Description: gets the number of bombs
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.numMines
    
    def getProfit(self) -> float:
        """
        Description: gets the profit
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return round(self.profit, 2)
    
    def getBalanceBeforeChange(self) -> float:
        """
        Description: gets the balance before change
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.balanceBeforeChange

    def getCurrentBalance(self) -> float:
        """
        Description: gets the current balance
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.wallet.get_balance()

    def increase_balance(self, amount) -> None:
        """
        Description: increases the balance
        Time Complexity:
            - O(1): All operations run in constant time
        """
        new_amount = self.wallet.increase_balance(amount)
        self.header.update_balance(new_amount)

