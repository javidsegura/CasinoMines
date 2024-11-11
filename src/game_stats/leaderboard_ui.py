""" Controls the leaderboard tab of the game """

from game_stats.data import UserData
from design.game_css import GameStyle
from others.algorithms.searching import MySearching

import pandas as pd 

from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QFontMetrics


class LeaderBoardTab(QWidget):
    def __init__(self, user_data:UserData) -> None:

        super().__init__()
        self.setStyleSheet(GameStyle().get_stylesheet())

        self.user_data = user_data
        self.leaderboard_pd = self.user_data.leaderboard_pd

        self.headers = []
        self.leaders = []
        self.firstRowFont = QFont("Arial", 50, QFont.Bold)
        self.valueFont = QFont("Arial", 40)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Top layout
        self.top_layout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.populateTopBar()
        self.top_layout.addWidget(self.small_text, alignment=Qt.AlignCenter)

        # Button container
        self.buttonContainer = QVBoxLayout()
        self.searchButton = QPushButton("Find my Rank")
        self.searchButton.clicked.connect(self.search)  # Connect to click event
        self.buttonContainer.addWidget(self.searchButton, alignment=Qt.AlignCenter)

        # Grid container
        self.grid_container = QWidget()
        self.grid_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contWidth = self.grid_container.width()

        # Left layout - Ranking
        self.left_layout = QGridLayout()
        self.left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.left_layout.setHorizontalSpacing(50)
        self.left_layout.setVerticalSpacing(40)

        # Right layout - Podium
        self.right_layout = QVBoxLayout()
        self.right_layout.addStretch()
        self.populatePodium()
        self.right_layout.addStretch()

        # Left and right layout (compacted to the grid container)
        self.left_right_layout = QHBoxLayout()
        self.left_right_layout.addLayout(self.left_layout)
        self.left_right_layout.addLayout(self.right_layout)

        self.grid_container.setLayout(self.left_right_layout)

        # Connecting to the main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.buttonContainer)
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)
    
    # 0. Top-bar (top layout)
    def populateTopBar(self) -> None:
        """ Populate the headers of the leaderboard tab"""

        title = QLabel("LeaderBoard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 50px; font-weight: bold;")

        self.small_text = QLabel(f"Total Players: {self.user_data.return_numPlayers() + 1}")
        self.small_text.setStyleSheet("font-size: 15px;")
        self.small_text.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.title_layout.addStretch()
        self.title_layout.addWidget(title)
        self.title_layout.addStretch()
        self.top_layout.addLayout(self.title_layout)

    # 1. Ranking (left layout)
    def populateRanking(self, start:int=0, limit:int=0, userRow:int=None, searchRank:bool=False) -> None:
        """ Populate the ranking. Run at the beggining and when the user clicks on the search button (flag is self.searchRank = True)
        Paremeters:
            start (int): The starting row to filter from
            limit (int): The ending row to filter to
            userRow (int): The row of the user in the ranking
        """
        
        self.clearData()
        
        # Are these two lines necessary?
        leaderData = pd.read_csv(self.user_data.leaderboardPath)
        leaderDataList = leaderData.values.tolist()
        numPlayers = leaderData.shape[0]

        if not searchRank:
            limit = numPlayers 
            if numPlayers > 10: # If more than 10 players, only show top 10
                limit = 10
        searchRank = False

        # Populate the ranking headers
        rankingCol = 0
        for col in ["Rank", "User", "Top Balance", "Date"]:
            value_label = QLabel(col)
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setFont(self.firstRowFont)
            self.left_layout.addWidget(value_label, 0, rankingCol)
            rankingCol += 1
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.main_layout.addItem(spacer)
            self.setLayout(self.main_layout)

        # Populate the ranking values
        for row in range(start, limit): 
            if row <= numPlayers:
                print(f"Row: {row}, leaderData: {leaderDataList}")
                rowData = leaderDataList[row]
                for col, value in enumerate(rowData): # e.g: (0, rank), (1, username), (2, largestBalance), (3, date)

                    print(f"\tRow: {row}, Col: {rowData[col]}, Value: {value}")
                   
                    value_label = QLabel(str(value)) # QLabel need to be str
                    value_label.setAlignment(Qt.AlignCenter)
                    value_label.setFont(self.valueFont)

                    # Highlight the user's row
                    if row == userRow:
                        value_label.setStyleSheet("background-color: #ffcc00; color: white;")

                    self.left_layout.addWidget(value_label, row, col)

            print(f"\nAdded user data to the grid")
            print("\n","-"*30, "\n")

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)

        # Every time the ranking is populated, the podium is updated automatically
        self.populatePodium()
    
    # 2. Podium (right layout)
    def populatePodium(self) -> None:
        """ Invoked from populateRanking()"""

        # Clear the right layout
        self.clearData(False)

        try:
            ogPixmap = QPixmap("./utils/imgs/podium.png")
            pixmap = ogPixmap.scaled(int(self.contWidth), 500, Qt.KeepAspectRatio)
            self.image_label = QLabel()
        except FileNotFoundError:
            print("Podium image not found")

        shiftUnit = self.contWidth // 10 #on freeform there are about 10 equally spaced apart units across the image
        
        df = pd.read_csv(self.user_data.leaderboardPath)
        print(f"df: {df.to_string()}")
        podium_ranking = df.values.tolist()

        print(f"Podium ranking: {podium_ranking}")

        painter = QPainter(pixmap)
        painter.setPen("white")

        for i in range(len(podium_ranking)):
            if i == 0:
                font = QFont("Arial", 35)
                fontMetrics = QFontMetrics(font)
                firstPlace_username = podium_ranking[0][1]
                firstPlace_textWidth = fontMetrics.horizontalAdvance(firstPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit * 5) - (firstPlace_textWidth // 2), 25, firstPlace_username) #finding string width in pixels and adjusting position on image
                print(f"First place username: {firstPlace_username}")

            elif i == 1:
                font = QFont("Arial", 30)
                fontMetrics = QFontMetrics(font)
                secondPlace_username = podium_ranking[1][1]
                secondPlace_textWidth = fontMetrics.horizontalAdvance(secondPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit * 2) - (secondPlace_textWidth // 2), 25, secondPlace_username)
                print(f"Second place username: {secondPlace_username}")

            elif i == 2:
                font = QFont("Arial", 20)
                fontMetrics = QFontMetrics(font)
                thirdPlace_username = podium_ranking[2][1]
                thirdPlace_textWidth = fontMetrics.horizontalAdvance(thirdPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit*8.5) - (thirdPlace_textWidth // 2), 32, thirdPlace_username)
                print(f"Third place username: {thirdPlace_username}")
            else:
                break

        painter.end()

        self.image_label.setPixmap(pixmap)
        self.right_layout.addWidget(self.image_label, alignment=Qt.AlignCenter | Qt.AlignVCenter)


    # 3. Auxiliary functions
    def search(self) -> None:
        """ Search for the user in the leaderboard and populate the ranking """

        # Previously we were doing a linear search, now we do a binary search
        search = MySearching()
        userRank, start, limit = search.binary_search_leaderboard(self.leaderboard_pd.values.tolist(), self.username)

        if userRank != -1:
            self.populateRanking(start, limit, userRank, searchRank=True)
        else:
            QMessageBox.warning(self, f"{self.username} is not on the leaderboard yet", "Play a game or log in with your previous username!")



    def clearData(self, left=True) -> None:
        """ Remove users from podium
        Parameters:
            left (bool): Whether to clear the left layout or the right layout
        """
        if left:
            while self.left_layout.count():
                item = self.left_layout.takeAt(0)  # Take the item at the top of the layout
                if item.widget():  # Check if the item is a widget
                    item.widget().deleteLater() # delete row 
        else:
            while self.right_layout.count():
                item = self.right_layout.takeAt(0)
                if item.widget(): 
                    item.widget().deleteLater()
    
    def defineUsername(self, user: str) -> None:
        """ comes given after the user logs in"""
        self.username = user


                        

                    


    
    