""" Controls the leaderboard tab of the game """

from game_tabs.data import UserData
from others.algorithms.searching import MySearching
from others.algorithms.sorting import MySorting

import pandas as pd 

from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QFontMetrics, QColor, QPen


class LeaderBoardTab(QWidget):
    def __init__(self, user_data:UserData) -> None:
        """ Initilaizes the leaderboard stats Tab
        Time Complexity:
            - O(n): because of the populatePodium() call
        """
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
        self.populateTopBar() # O(1)
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

        # Left layout and container - Ranking
        self.left_layout = QGridLayout()
        self.left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.left_layout.setHorizontalSpacing(50)
        self.left_layout.setVerticalSpacing(40)
        self.left_container = QWidget()
        self.left_container.setLayout(self.left_layout)
        self.left_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contHeight = self.left_container.height()

        # Right layout and container - Podium
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.right_container = QWidget()
        self.right_container.setLayout(self.right_layout)
        self.populatePodium() # O(n)
        self.right_container.setMaximumHeight(self.contHeight // 1.5)
        self.right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Left and right layout (compacted to the grid container)
        self.left_right_layout = QHBoxLayout()
        self.left_right_layout.addWidget(self.left_container, stretch=1)
        self.left_right_layout.addWidget(self.right_container, stretch=1)

        # Connecting to the main layout
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.buttonContainer)
        self.main_layout.addLayout(self.left_right_layout)

        self.main_layout.addStretch()

        self.setLayout(self.main_layout)
    
    # 0. Top-bar (top layout)
    def populateTopBar(self) -> None:
        """ Populate the headers of the leaderboard tab
        Time Complexity:
            - O(1): All operations run in constant time
        """

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
        Time Complexity:
            - O(n*m): where one n is the number of rows in the leaderboard and m is the number of columns in the leaderboard
        """
        
        self.clearData()
        
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
        for row_idx, data_row in enumerate(range(start, limit)): # O(n)
            if data_row < numPlayers: 
                rowData = leaderDataList[data_row]
                for col, value in enumerate(rowData): # O(n)
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
        """ Draws the top 3 users in the leaderboard onto the podium image
        Time Complexity:
            - O(n): for the clearData() call and the setting in the podium. The latter relies on pure asymtotic analysis
                and ignores that the podium has a fixed size.
        """

        # Clear the right layout
        self.clearData(False)

        try:
            ogPixmap = QPixmap("./utils/imgs/podium.png")
            scaled_pixmap = ogPixmap.scaled(int(self.contWidth), 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            black_image = QPixmap(scaled_pixmap.width(), 100) #dummy pixmap to write text above "scaled_pixmap"
            black_image.fill(QColor(10, 0, 26))

            self.image_label = QLabel()
            self.fill_label = QLabel()
        except FileNotFoundError:
            print("Podium image not found")

        
        df = pd.read_csv(self.user_data.leaderboardPath)
        podium_ranking = df.values.tolist()

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

        for i in range(len(podium_ranking)-1):
            if i == 0:
                font = QFont("Arial", 35)
                firstPlace_username = self.leaderboard_pd.iloc[0]['username']
                firstPlace.setFont(font)
                firstPlace.drawText(black_image.rect(), Qt.AlignCenter | Qt.AlignBottom, firstPlace_username)

            elif i == 1:
                font = QFont("Arial", 35)
                fontMetrics = QFontMetrics(font)
                secondPlace_username = self.leaderboard_pd.iloc[1]['username']
                secondPlace_textWidth = fontMetrics.horizontalAdvance(secondPlace_username)
                painter.setFont(font)
                painter.drawText((shiftUnit * 8) - (secondPlace_textWidth // 2) - 40, 65, secondPlace_username)

            elif i == 2:
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

    # 3. Auxiliary functions
    def search(self) -> None:
        """ Search for the user in the sorted leaderboard (by name) using binary search 
            and populate the ranking
        Time Complexity:
            - O(n * log n): where n is the number of rows in the leaderboard
        """
        sortedByName = self.leaderboardSortedByName()

        search = MySearching()
        userRank = search.binary_search_leaderboard(sortedByName, self.username)

        if userRank != -1:
            username = self.username
            start = 1
            if userRank > 5: 
                start = userRank - 4
            limit = start + 9

            self.populateRanking(start, limit, username, searchRank=True)
        else:
            QMessageBox.warning(self, f"{self.username} is not on the leaderboard yet", "Play a game or log in with your previous username!")

    def clearData(self, left=True) -> None:
        """ Remove users from podium
        Parameters:
            left (bool): Whether to clear the left layout or the right layout
        Time Complexity:
            - O(n): where n is the number of elements in specified layout (left or right)
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
        """ Called after username defined at initilization of main.py
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.username = user

    def leaderboardSortedByName(self) -> list[tuple]:
        """ Sorts the leaderboard by name and returns it
        Time Complexity:
            - O(n * log n): where n is the number of rows in the leaderboard
        """
        sortedByName = self.user_data.leaderboard_pd.values.tolist()

        MySorting(1, ascending=False).mergeSort(sortedByName, 0, len(sortedByName)) # sorts in-place

        return sortedByName