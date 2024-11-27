from PySide6.QtWidgets import (QHBoxLayout, QLabel, QFrame)
from PySide6.QtGui import QFont

class Header:
    """ Defines the header element of the game"""
    def __init__(self) -> None:
        self.username_label = QLabel()
        self.wallet_label = QLabel()
        self.multiplier_label = QLabel()
        self.profit_label = QLabel()

    def setup_header(self) -> QFrame:
        header_layout = QHBoxLayout()  # Horizontal layout
        header_layout.setContentsMargins(10, 5, 10, 5)  # Set explicit margins
        header_layout.setSpacing(15)  # Adjusted for consistent spacing

        header_frame = QFrame()  # Frame to contain the header
        header_frame.setFixedHeight(50)  # Set a fixed height for the header
        header_frame.setStyleSheet("""
            background-color: #1a0033;  /* Darker purple */
            color: #c1cdcd;  /* Gold color for text */
            border-radius: 5px;
        """)
        header_frame.setLayout(header_layout)

        # Game name
        game_name_label = QLabel("CasinoMines")
        game_name_label.setFont(QFont("Arial", 12, QFont.Bold))  # Smaller font size
        game_name_label.setFixedHeight(30)  # Ensure consistent label height
        game_name_label.setStyleSheet("color: #c1cdcd;")  # Gold color for text
        header_layout.addWidget(game_name_label)

        # Spacer
        header_layout.addStretch()

        # Username
        self.username_label.setText("User: username")
        self.username_label.setFixedHeight(30)
        self.username_label.setStyleSheet("color: #c1cdcd;")  # Gold color for text
        header_layout.addWidget(self.username_label)

        header_layout.addSpacing(15)

        # Wallet balance
        self.wallet_label.setText("Balance: 1000$")
        self.wallet_label.setFixedHeight(30)
        self.wallet_label.setStyleSheet("color: #c1cdcd;")  # Gold color for text
        header_layout.addWidget(self.wallet_label)

        header_layout.addSpacing(15)

        # Current multiplier
        self.multiplier_label.setText("Multiplier: 1x")
        self.multiplier_label.setFixedHeight(30)
        self.multiplier_label.setStyleSheet("color: #c1cdcd;")  # Gold color for text
        header_layout.addWidget(self.multiplier_label)

        header_layout.addSpacing(15)

        # Profit
        self.profit_label.setText("Profit: 0$")
        self.profit_label.setFixedHeight(30)
        self.profit_label.setStyleSheet("color: #c1cdcd;")  # Gold color for text
        header_layout.addWidget(self.profit_label)

        return header_frame

    def update_balance(self, new_balance: float) -> None:
        self.wallet_label.setText(f"Balance: {round(new_balance, 2)}$")

    def update_multiplier(self, new_multiplier: float) -> None:
        self.multiplier_label.setText(f"Multiplier: {round(new_multiplier, 2)}x")

    def update_profit(self, new_profit: float) -> None:
        self.profit_label.setText(f"Profit: {round(new_profit, 2)}$")

    def update_user(self, user: str) -> None:
        self.username_label.setText(f"User: {user}")
