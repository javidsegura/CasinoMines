""" Controls the leaderboard tab of the game """

from game_tabs.data import UserData
from others.algorithms.searching import MySearching

import pandas as pd 

from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QMessageBox, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QFontMetrics, QColor
from PySide6.QtGui import QFont, QPixmap, QPainter, QFontMetrics, QColor, QPen

# Leaderboard should be a set
class LeaderBoardTab(QWidget):
    def __init__(self, user_data:UserData) -> None:

        super().__init__()

        self.user_data = user_data
        self.leaderboard_pd = self.user_data.leaderboard_pd
        self.leaderboard_dict = None
        self.userSortLeaderboard = None
        self.username = None

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

        # Left layout + container for Ranking
        self.left_layout = QGridLayout()
        self.left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.left_layout.setHorizontalSpacing(50)
        self.left_layout.setVerticalSpacing(40)
        self.left_container = QWidget()
        self.left_container.setLayout(self.left_layout)
        self.left_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right layout + container for Podium
        self.right_layout = QVBoxLayout()
        self.right_layout.addStretch()
        self.right_container = QWidget()
        self.right_container.setLayout(self.right_layout)
        self.right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.populatePodium()

        # Left and right layout (compacted to the grid container)
        self.left_right_layout = QHBoxLayout()
        self.left_right_layout.addWidget(self.left_container)
        self.left_right_layout.addWidget(self.right_container)

        self.grid_container.setLayout(self.left_right_layout)

        # Connecting to the main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.buttonContainer)
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)
    
    def updateVars(self, leaderboard_dict:dict, leaderboard_df:pd.DataFrame, userSortLeaderboard:pd.DataFrame, username:str) -> None:
        self.leaderboard_dict = leaderboard_dict
        self.leaderboard_pd = leaderboard_df
        self.userSortLeaderboard = userSortLeaderboard
        self.username = username

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
    def populateRanking(self, start:int=0, limit:int=0, username:str=None, searchRank:bool=False, rank:int=0) -> None:
        """ Populate the ranking. Run at the beggining and when the user clicks on the search button (flag is self.searchRank = True)
        Paremeters:
            start (int): The starting row to filter from
            limit (int): The ending row to filter to
            username (str): The username of the user
            searchRank (bool): Whether the ranking is being searched or not
        """
        self.leaderboard_pd, self.leaderboard_dict, self.userSortLeaderboard = self.user_data.getChangedVars()
        
        self.clearData()
        
        numPlayers = self.leaderboard_pd.shape[0]

        if not searchRank:
            limit = numPlayers 
            if numPlayers > 10: # If more than 10 players, only show top 10
                limit = 10
        else:
            if rank - 4 < 1:
                start = 0
            else:
                start = rank - 4
            if rank + 5 > numPlayers:
                limit = numPlayers
            else:
                limit = rank + 5

        # Populate the ranking headers
        rankingCol = 0
        for col in ["Rank", "User", "Top Balance", "Date"]:
            value_label = QLabel(str(col))
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setFont(self.firstRowFont)
            self.left_layout.addWidget(value_label, 0, rankingCol)
            rankingCol += 1
            
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)

        if start != 0:
            start -= 1

        # Populate the ranking values
        for row_idx, data_row in enumerate(range(start, limit)):

            if data_row < numPlayers:  # Changed <= to < to prevent index out of range
                rowData = self.leaderboard_pd.iloc[data_row]
                print(f"Id {data_row} rowData {rowData}")

                columns = ['rank', 'username', 'largestBalance', 'date']
                for col_idx, col_name in enumerate(columns):
                    value = rowData[col_name]
                    value_label = QLabel(str(value)) 
                    value_label.setAlignment(Qt.AlignCenter)
                    value_label.setFont(self.valueFont)

                    # Highlight the user's row
                    if col_name == 'username' and value == self.username:
                        value_label.setStyleSheet("background-color: #ffcc00; color: #00001a;")

                    # Use row_idx + 1 to place data right below headers
                    self.left_layout.addWidget(value_label, row_idx + 1, col_idx)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)

        # Update podium based on the new ranking
        if not searchRank:
            self.populatePodium()
    
    # 2. Podium (right layout)
    def populatePodium(self) -> None:
        """ Invoked from populateRanking()"""

        # Clear the right layout
        self.clearData(False)

        try:
            ogPixmap = QPixmap("./utils/imgs/podium.png")
            scaled_pixmap = ogPixmap.scaled(int(self.contWidth), 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            black_image = QPixmap(scaled_pixmap.width(), 500) #dummy pixmap to write text above "scaled_pixmap"
            black_image.fill(QColor(0, 0, 26))

            self.image_label = QLabel()
            self.fill_label = QLabel()
        except FileNotFoundError:
            print("Podium image not found")

        pen = QPen(QColor("#ffcc00"))
        firstPlace = QPainter(black_image)
        firstPlace.setRenderHint(QPainter.Antialiasing)
        firstPlace.setRenderHint(QPainter.SmoothPixmapTransform)
        firstPlace.setPen(pen)

        painter = QPainter(scaled_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.setPen(pen)
        shiftUnit = self.contWidth / 9 

        for i in range(len(self.leaderboard_pd)):
            if i == 0: #first place
                font = QFont("Arial", 35)
                firstPlace_username = self.leaderboard_pd.iloc[0]['username']
                firstPlace.setFont(font)
                firstPlace.drawText(black_image.rect(), Qt.AlignCenter | Qt.AlignBottom, firstPlace_username)

            elif i == 1: #second place
                font = QFont("Arial", 35)
                fontMetrics = QFontMetrics(font)
                secondPlace_username = self.leaderboard_pd.iloc[1]['username']
                secondPlace_textWidth = fontMetrics.horizontalAdvance(secondPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit * 8) - (secondPlace_textWidth // 2) - 40, 65, secondPlace_username)

            elif i == 2: #third place
                font = QFont("Arial", 25)
                fontMetrics = QFontMetrics(font)
                thirdPlace_username = self.leaderboard_pd.iloc[2]['username']
                thirdPlace_textWidth = fontMetrics.horizontalAdvance(thirdPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit*2) - (thirdPlace_textWidth // 2) - 25, 110, thirdPlace_username)
            else:
                break

        painter.end()
        firstPlace.end()

        self.image_label.setPixmap(scaled_pixmap)
        self.fill_label.setPixmap(black_image)
        self.image_label.setScaledContents(False)
        self.fill_label.setScaledContents(False)


        self.right_layout.addWidget(self.fill_label, alignment=Qt.AlignVCenter)
        self.right_layout.addWidget(self.image_label, alignment=Qt.AlignVCenter)
        self.right_layout.setSpacing(0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

    # 3. Auxiliary functions
    def search(self) -> None:
        """ Search for the user in the leaderboard and populate the ranking """

        # Update variables according to new leaderboard
        self.leaderboard_pd, self.leaderboard_dict, self.userSortLeaderboard = self.user_data.getChangedVars()

        # Search for the user in the leaderboard
        search = MySearching()
        user_rank = search.binary_search_users(self.userSortLeaderboard, self.username)
        print(f"User {self.username} is in: {user_rank}")
        self.populateRanking(0, 0, self.username, True, user_rank)


    def clearData(self, left=True) -> None:
        """ Remove users from podium
        Parameters:
            left (bool): Whether to clear the left layout or the right layout
        """

        if left:
            while self.left_layout.count():
                item = self.left_layout.takeAt(0)  
                if item.widget():  
                    item.widget().deleteLater() 
        else:
            while self.right_layout.count():
                item = self.right_layout.takeAt(0)
                if item.widget(): 
                    item.widget().deleteLater()
    
    def defineUsername(self, user:str) -> None:
        """ comes given after the user logs in"""
        self.username = user


                        

                    


    
    