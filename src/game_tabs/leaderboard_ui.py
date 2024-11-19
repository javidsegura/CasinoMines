""" Controls the leaderboard tab of the game """

from game_tabs.data import UserData
from others.algorithms.searching import MySearching

import pandas as pd 

from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QMessageBox, QGridLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QFontMetrics, QColor


class LeaderBoardTab(QWidget):
    def __init__(self, user_data:UserData) -> None:

        super().__init__()

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

        # Left layout + container - Ranking
        self.left_layout = QGridLayout()
        self.left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.left_layout.setHorizontalSpacing(50)
        self.left_layout.setVerticalSpacing(40)
        self.left_container = QWidget()
        self.left_container.setLayout(self.left_layout)
        self.left_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right layout + container - Podium
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
    def populateRanking(self, start:int=0, limit:int=0, username:str=None, searchRank:bool=False) -> None:
        """ Populate the ranking. Run at the beggining and when the user clicks on the search button (flag is self.searchRank = True)
        Paremeters:
            start (int): The starting row to filter from
            limit (int): The ending row to filter to
            username (str): The username of the user
            searchRank (bool): Whether the ranking is being searched or not
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
                rowData = leaderDataList[data_row]
                for col, value in enumerate(rowData):
                    value_label = QLabel(str(value)) 
                    value_label.setAlignment(Qt.AlignCenter)
                    value_label.setFont(self.valueFont)

                    # Highlight the user's row
                    if rowData[1] == username:
                        value_label.setStyleSheet("background-color: #ffcc00; color: white;")

                    # Use row_idx + 1 to place data right below headers
                    self.left_layout.addWidget(value_label, row_idx + 1, col)

            

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
            black_image.fill(QColor(43, 43, 43))

            self.image_label = QLabel()
            self.fill_label = QLabel()
        except FileNotFoundError:
            print("Podium image not found")

        firstPlace = QPainter(black_image)
        firstPlace.setRenderHint(QPainter.Antialiasing)
        firstPlace.setRenderHint(QPainter.SmoothPixmapTransform)
        firstPlace.setPen("white")

        df = pd.read_csv(self.user_data.leaderboardPath)
        podium_ranking = df.values.tolist()

        painter = QPainter(scaled_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.setPen("white")
        shiftUnit = self.contWidth / 9 

        for i in range(len(podium_ranking)):
            if i == 0: #first place
                font = QFont("Arial", 35)
                firstPlace_username = podium_ranking[0][1]
                firstPlace.setFont(font)
                firstPlace.drawText(black_image.rect(), Qt.AlignCenter | Qt.AlignBottom, firstPlace_username)

            elif i == 1: #second place
                font = QFont("Arial", 35)
                fontMetrics = QFontMetrics(font)
                secondPlace_username = podium_ranking[1][1]
                secondPlace_textWidth = fontMetrics.horizontalAdvance(secondPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit * 8) - (secondPlace_textWidth // 2) - 40, 65, secondPlace_username)

            elif i == 2: #third place
                font = QFont("Arial", 25)
                fontMetrics = QFontMetrics(font)
                thirdPlace_username = podium_ranking[2][1]
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


        self.right_layout.addWidget(self.fill_label, alignment=Qt.AlignBottom)
        self.right_layout.addWidget(self.image_label, alignment=Qt.AlignBottom)
        self.right_layout.setSpacing(0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)

    # 3. Auxiliary functions
    def search(self) -> None:
        """ Search for the user in the leaderboard and populate the ranking """

        # Find the user rank
        df = pd.read_csv(self.user_data.leaderboardPath)

        if self.username in set(df['username'].values): 
        #Converting to set is still O(n), but we need to check if username exists before 
        #assigining a value otherwise will get an error. Only way around is to pre-save each user's rank,
        #but this is dynamic and will change very often
            
            userRank = df[df["username"] == self.username]["rank"].values[0]
            # Search for the user in the leaderboard
            search = MySearching()
            username, start, limit = search.binary_search_leaderboard(df.values.tolist(), userRank)

            if username != -1:
                self.populateRanking(start, limit, username, searchRank=True)
            else:
                QMessageBox.warning(self, f"{self.username} is not on the leaderboard yet", "Play a game or log in with your previous username!")
        else:
            QMessageBox.warning(self, f"{self.username} is not on the leaderboard yet", "Play a game or log in with your previous username!")

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


                        

                    


    
    