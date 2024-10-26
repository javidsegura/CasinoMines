from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame, QMessageBox, QTabWidget, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from game_css import GameStyle
from data import UserData

import csv


class LeaderBoardTab(QWidget):
    def __init__(self, user_data, file_path="utils/data/userData.csv"):
        super().__init__()
        self.setStyleSheet(GameStyle().get_stylesheet())

        self.user_data = user_data
        self.numPlayers = self.user_data.return_numPlayers()
        print(f"Num Players is {self.numPlayers}")
        self.leaderData = self.user_data.return_leaderboard_list()
        print(f"Leaderboard is {self.leaderData}")

        self.headers = []
        self.leaders = []
        self.firstRowFont = QFont("Arial", 20, QFont.Bold)
        self.valueFont = QFont("Arial", 20)
        self.mapping = {
            "rank": "Rank",
            "user": "User",
            "largestBalance": "Top Balance"
        }


        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.top_layout = QHBoxLayout()
        self.populateHeaders()

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.grid_layout.setHorizontalSpacing(50)
        self.grid_layout.setVerticalSpacing(30)

        self.grid_container = QWidget()
        self.grid_container.setLayout(self.grid_layout)
        self.grid_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Set the layout for the DataTab
        self.main_layout.addLayout(self.top_layout)

        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addStretch()

        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
    
    def populateHeaders(self):
        title = QLabel("LeaderBoard")
        title.setAlignment(Qt.AlignCenter)
        titleFont = QFont("Arial", 50, QFont.Bold)
        title.setFont(titleFont)

        small_text = QLabel(f"Players: {self.numPlayers}")
        small_font = QFont("Arial", 12)
        small_text.setFont(small_font)
        small_text.setAlignment(Qt.AlignRight | Qt.AlignTop)
        # , alignment=Qt.AlignCenter
        # , alignment=Qt.AlignRight
        self.top_layout.addStretch()
        self.top_layout.addWidget(title)
        self.top_layout.addStretch()
        self.top_layout.addWidget(small_text)

    def populateLeaders(self):
        self.leaderData = self.user_data.return_leaderboard_list()
        print(f"LeaderData in populateleaders: {self.leaderData}")
        for row, rowData in enumerate(self.leaderData):
            for col, value in enumerate(rowData):
                if row == 0:
                    # if col == 0:
                    #     value_label = QLabel("Rank")
                    # else:
                    value_label = QLabel(self.mapping[value])
                    value_label.setAlignment(Qt.AlignCenter)
                    value_label.setFont(self.firstRowFont)
                    self.grid_layout.addWidget(value_label, row, col)
                else:
                    if col == 0:
                        value_label = QLabel(str(value))
                    else:
                        value_label = QLabel(value)
                    value_label.setAlignment(Qt.AlignCenter)
                    value_label.setFont(self.valueFont)
                    self.grid_layout.addWidget(value_label, row, col)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
        
                        

                    


    
    