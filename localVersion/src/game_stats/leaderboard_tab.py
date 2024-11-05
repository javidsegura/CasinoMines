""" Controls the leaderboard tab of the game """

from design.game_css import GameStyle
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QMessageBox, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QPainter, QFontMetrics

class LeaderBoardTab(QWidget):
    def __init__(self, user_data) -> None:
        super().__init__()
        self.setStyleSheet(GameStyle().get_stylesheet())

        self.user_data = user_data
        self.numPlayers = self.user_data.return_numPlayers()
        self.leaderData = self.user_data.return_leaderboard_list()

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
        self.searchButton = QPushButton("Find my Rank")
        self.searchButton.clicked.connect(self.search)  # Connect to click event
        self.buttonContainer.addWidget(self.searchButton, alignment=Qt.AlignCenter)

        self.grid_container = QWidget()
        self.grid_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.contWidth = self.grid_container.width()

        self.left_layout = QGridLayout()
        self.left_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.left_layout.setHorizontalSpacing(50)
        self.left_layout.setVerticalSpacing(40)

        self.right_layout = QVBoxLayout()
        self.right_layout.addStretch()
        self.populatePodium()
        self.right_layout.addStretch()

        self.left_right_layout = QHBoxLayout()
        self.left_right_layout.addLayout(self.left_layout)
        self.left_right_layout.addLayout(self.right_layout)

        self.grid_container.setLayout(self.left_right_layout)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.buttonContainer)
        self.main_layout.addWidget(self.grid_container)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)
    
    def populateHeaders(self) -> None:
        title = QLabel("LeaderBoard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 50px; font-weight: bold;")

        self.small_text = QLabel(f"Players: {self.numPlayers}")
        self.small_text.setStyleSheet("font-size: 15px;")
        self.small_text.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.title_layout.addStretch()
        self.title_layout.addWidget(title)
        self.title_layout.addStretch()
        self.top_layout.addLayout(self.title_layout)

    def populateLeaders(self, start=1, limit=0, userRow=None) -> None:
        self.clearData()
        self.leaderData = self.user_data.return_leaderboard_list()
        #print(f"LeaderData in populated leaders: {self.leaderData}")

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
            self.left_layout.addWidget(value_label, 0, headerCol)
            headerCol += 1
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.main_layout.addItem(spacer)
            self.setLayout(self.main_layout)

        # print(f"Start: {start} {self.leaderData[start]} End: {limit} {self.leaderData[limit]}")
        for row in range(start, limit + 1): # +1 for label row
            if row <= self.numPlayers:
                rowData = self.leaderData[row]
                for col, value in enumerate(rowData):
                    if col == 0:
                        value_label = QLabel(str(value))
                    else:
                        value_label = QLabel(value)
                    value_label.setAlignment(Qt.AlignCenter)
                    value_label.setFont(self.valueFont)
                    if row == userRow:
                        value_label.setStyleSheet("background-color: #ffcc00; color: white;")
                    self.left_layout.addWidget(value_label, row, col)
                
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
        self.populatePodium()
    
    def populatePodium(self) -> None:
        self.clearData(False)
        try:
            ogPixmap = QPixmap("localVersion/utils/imgs/podium.png")
            pixmap = ogPixmap.scaled(int(self.contWidth), 500, Qt.KeepAspectRatio)
            self.image_label = QLabel()
        except FileNotFoundError:
            print("Podium image not found")

        shiftUnit = self.contWidth // 10 #on freeform there are about 10 equally spaced apart units across the image
        # not perfect but pretty good
        top3 = {}
        for i in range(1, self.numPlayers + 2): #plus two for index change and title row
            if i < len(self.leaderData):
                if i > 3:
                    break
                top3[i] = self.leaderData[i][1]
            else:
                break

        painter = QPainter(pixmap)
        painter.setPen("white")

        if 1 in top3:
            font = QFont("Arial", 35)
            fontMetrics = QFontMetrics(font)
            text = top3[1]
            textWidth = fontMetrics.horizontalAdvance(text)
            painter.setFont(font)
            painter.drawText((shiftUnit * 5) - (textWidth // 2), 25, text) #finding string width in pixels and adjusting position on image

            if 2 in top3:
                font = QFont("Arial", 30)
                fontMetrics = QFontMetrics(font)
                text = top3[2]
                textWidth = fontMetrics.horizontalAdvance(text)
                painter.setFont(font)
                painter.drawText((shiftUnit * 2) - (textWidth // 2), 25, text)
                if 3 in top3:
                    font = QFont("Arial", 20)
                    fontMetrics = QFontMetrics(font)
                    text = top3[3]
                    textWidth = fontMetrics.horizontalAdvance(text)
                    painter.setFont(font)
                    painter.drawText((shiftUnit*8.5) - (textWidth // 2), 32, text)

        painter.end()

        self.image_label.setPixmap(pixmap)
        self.right_layout.addWidget(self.image_label, alignment=Qt.AlignCenter | Qt.AlignVCenter)

    def defineUsername(self, user: str) -> None:
        self.username = user

    def search(self) -> None:
        self.numPlayers = self.user_data.return_numPlayers()

        for person in self.leaderData:
            if person[1] == self.username:
                #print(f"{self.username} is {person[0]} place!")
                
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

    def clearData(self, left=True) -> None:
        if left:
            while self.left_layout.count():
                item = self.left_layout.takeAt(0)  # Take the item at the top of the layout
                if item.widget():  # Check if the item is a widget
                    item.widget().deleteLater()
        else:
            while self.right_layout.count():
                item = self.right_layout.takeAt(0)
                if item.widget(): 
                    item.widget().deleteLater()


                        

                    


    
    