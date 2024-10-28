from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame, QMessageBox, QTabWidget, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QPalette
from game_css import GameStyle

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

        self.username = None
        self.searched = False
        self.headers = []
        self.leaders = []
        self.firstRowFont = QFont("Arial", 50, QFont.Bold)
        self.valueFont = QFont("Arial", 40)
        self.mapping = {
            "rank": "Rank",
            "user": "User",
            "largestBalance": "Top Balance"
        }


        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.top_layout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.populateHeaders()
        self.top_layout.addWidget(self.small_text, alignment=Qt.AlignCenter)


        self.buttonContainer = QVBoxLayout()
        # self.buttonContainer.setAlignment(Qt.AlignTop) ??
        self.searchButton = QPushButton("Find my Rank")
        self.searchButton.clicked.connect(self.search)  # Connect to click event

        self.buttonContainer.addWidget(self.searchButton, alignment=Qt.AlignCenter)


        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.grid_layout.setHorizontalSpacing(50)
        self.grid_layout.setVerticalSpacing(40)

        self.right_layout = QVBoxLayout()
        # self.right_test = QLabel("test")
        self.populatePodium()
        # self.right_test.setAlignment(Qt.AlignCenter)
        # self.right_layout.addWidget(self.right_test, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.right_layout.addStretch()

        self.left_right_layout = QHBoxLayout()
        self.left_right_layout.addLayout(self.grid_layout)
        self.left_right_layout.addLayout(self.right_layout)
        # self.left_right_layout.addStretch()


        self.grid_container = QWidget()
        self.grid_container.setLayout(self.left_right_layout)
        self.grid_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set the layout for the DataTab
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.buttonContainer)
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addStretch()

        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
    
    def populateHeaders(self):
        title = QLabel("LeaderBoard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 50px; font-weight: bold;")

        self.small_text = QLabel(f"Players: {self.numPlayers}")
        self.small_text.setStyleSheet("font-size: 15px;")
        self.small_text.setAlignment(Qt.AlignRight | Qt.AlignTop)
        # , alignment=Qt.AlignCenter
        # , alignment=Qt.AlignRight
        self.title_layout.addStretch()
        self.title_layout.addWidget(title)
        self.title_layout.addStretch()
        self.top_layout.addLayout(self.title_layout)

    def populateLeaders(self, start=1, limit=0, userRow=None):
        self.clearData()
        self.leaderData = self.user_data.return_leaderboard_list()
        print(f"LeaderData in populateleaders: {self.leaderData}")

        self.numPlayers = self.user_data.return_numPlayers()

        if not self.searched:
            limit = self.numPlayers 
            if self.numPlayers > 10:
                limit = 10
        self.searched = False

        headerCol = 0
        for value in self.leaderData[0]:
            value_label = QLabel(self.mapping[value])
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setFont(self.firstRowFont)
            self.grid_layout.addWidget(value_label, 0, headerCol)
            headerCol += 1
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.main_layout.addItem(spacer)
            self.setLayout(self.main_layout)

        print(f"Start: {start} {self.leaderData[start]} End: {limit} {self.leaderData[limit]}")
        for row in range(start, limit + 1): # +1 for label row
            rowData = self.leaderData[row]
            print(f"Row data: {rowData}")
            for col, value in enumerate(rowData):
                if col == 0:
                    value_label = QLabel(str(value))
                else:
                    value_label = QLabel(value)
                value_label.setAlignment(Qt.AlignCenter)
                value_label.setFont(self.valueFont)
                if row == userRow:
                    print("Yurrr")
                    value_label.setStyleSheet("background-color: #ffcc00; color: white;")
                self.grid_layout.addWidget(value_label, row, col)
                
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
    
    def populatePodium(self):
        ogPixmap = QPixmap("utils/imgs/podium.png")
        pixmap = ogPixmap.scaled(500, 500, Qt.KeepAspectRatio)
        self.image_label = QLabel()
        
        painter = QPainter(pixmap)
        painter.setPen("white")
        painter.setFont(QFont("Arial", 30))
        painter.drawText(80, 25, "2nd")
        painter.setFont(QFont("Arial", 35))
        painter.drawText(250, 22, "1st")
        painter.setFont(QFont("Arial", 20))
        painter.drawText(410, 32, "3rd")
        painter.end()

        # self.add_text_to_pixmap(pixmap, "Overlayed Text", x=30, y=30)
        self.image_label.setPixmap(pixmap)
        self.right_layout.addWidget(self.image_label, alignment=Qt.AlignCenter | Qt.AlignVCenter)

    def defineUsername(self, user):
        self.username = user

    def search(self):
        self.numPlayers = self.user_data.return_numPlayers()
        print(f"{self.username} clicked the button! Num players: {self.numPlayers}")
        for person in self.leaderData:
            if person[1] == self.username:
                print(f"{self.username} is {person[0]} place!")
                
                start = 1
                if int(person[0]) > 5:
                    start = int(person[0]) - 4
                limit = start + 9
                if self.numPlayers < limit:
                    limit = self.numPlayers
                
                self.searched = True
                self.populateLeaders(start, limit, int(person[0]))
                return
        
        QMessageBox.warning(self, f"{self.username} is not on the leaderboard yet", "Play a game or log in with your previous username!")

    def clearData(self):
        print("\nDeleting...")
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)  # Take the item at the top of the layout
            if item.widget():  # Check if the item is a widget
                item.widget().deleteLater()


                        

                    


    
    