from PySide6.QtWidgets import (QHBoxLayout, QLabel, QFrame)
from PySide6.QtGui import QFont

class Header():
      """ Defines the header element of the game"""
      def __init__(self):
        self.username_label= QLabel()
        self.wallet_label = QLabel()
        self.multiplier_label = QLabel()
        self.profit_label = QLabel()

      def setup_header(self) -> QFrame:
        header_layout = QHBoxLayout() # Horizontal layout
        header_frame = QFrame() # Frame to contain the header
        header_frame.setStyleSheet("background-color: gray; color: white; border-radius: 5px;")
        header_frame.setLayout(header_layout)

        # Game name
        game_name_label = QLabel("CasinoMines")
        game_name_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_layout.addWidget(game_name_label)

        # Spacer
        header_layout.addStretch()

        # username
        self.username_label.setText("User:")
        header_layout.addWidget(self.username_label)

        header_layout.addSpacing(20)


        # Wallet balance
        self.wallet_label.setText("Balance: 1000$")
        header_layout.addWidget(self.wallet_label)

        # Spacer
        header_layout.addSpacing(20)

        # Current multiplier
        self.multiplier_label.setText("Multiplier: 1x")
        header_layout.addWidget(self.multiplier_label)

        # Profit
        self.profit_label.setText("Profit: 0$")
        header_layout.addWidget(self.profit_label)

        return header_frame
      
      def update_balance(self, new_balance):
        self.wallet_label.setText(f"Balance: {new_balance}$")

      def update_multiplier(self, new_multiplier):
        self.multiplier_label.setText(f"Multiplier: {new_multiplier}x")

      def update_profit(self, new_profit):
        print(f"Profit is {new_profit}")
        # self.profit = new_profit
        self.profit_label.setText(f"Profit: {round(new_profit,2)}$")

      def update_user(self, user):
        self.username_label.setText(f"Username: {user}")
        self.username_label.setStyleSheet("color: #00FF00;") 
