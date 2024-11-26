""" Controls the data tab of the game """

from design.game_css import GameStyle
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QGridLayout)
from PySide6.QtCore import Qt
from others.algorithms.sorting import MySorting
import csv
import math

class DataTab(QWidget):
    def __init__(self, file_path:str="./utils/data/game_stats.csv") -> None:
        super().__init__()
        self.setStyleSheet(GameStyle().get_stylesheet())
        
        self.file_path = file_path
        self.data = []
        self.headerButtons = []
        self.firstHeaderPop = True
        self.indexClicked = None

        self.mapping = {
            "win": "Win",
            "gameId": "Game ID",
            "betAmount": "Bet Amount",
            "numMines": "Number of Mines",
            "balanceBefore": "Balance Before",
            "balanceAfter": "Balance After",
            "profit": "Profit"
        }

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.populateHeaders()

        # Set the layout for the DataTab
        self.main_layout.addLayout(self.grid_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
    
    # give it a paramter with default none; if its not none then change that button backgorund to blue
    def populateHeaders(self) -> None:
        self.headerButtons = []
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for i, row in enumerate(csv_reader):
                for col, var in enumerate(row):
                    if i == 0:
                        header_button = QPushButton(self.mapping[var])  # Use QPushButton
                        header_button.setCheckable(True)
                        header_button.clicked.connect(lambda _, v=var, btn=header_button: self.headerClicked(v, btn))
                        if col == 0 and self.firstHeaderPop:
                            header_button.setStyleSheet("background-color: blue; color: white;")
                        # Set default dark purple for all header buttons
                        # header_button.setStyleSheet("background-color: #5A3D8A; color: white;")  # Slightly lighter dark purple
                        self.grid_layout.addWidget(header_button, 0, col)
                        self.headerButtons.append(header_button)

    def populateGameStats(self) -> None:
        """ Populate the values of the data tab"""
        self.clearData()
        self.firstHeaderPop = False
        for i, element in enumerate(self.headerButtons):
            if i == 0:
                element.setStyleSheet("background-color:  #2E0854;; color: white;")
            else:
                element.setStyleSheet("background-color:  #2E0854; color: white;")

        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            self.data = []
            self.data = list(csv_reader) #each time something is added to userData, self.data updates
            for row, rowData in enumerate(self.data):
                for col, var in enumerate(rowData):
                    if not row == 0:
                        value_label = QLabel(str(var))
                        value_label.setAlignment(Qt.AlignCenter)

                        if str(var) == "win":
                            value_label.setStyleSheet("background-color: lightgreen; color: black;")
                        elif str(var) == "loss":
                            value_label.setStyleSheet("background-color: lightcoral; color: black;")
                        self.grid_layout.addWidget(value_label, row, col)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
    
    def populateSortedValues(self, arr:list) -> None:
        sortedOutput = []
        for element in arr:
            currIndex = element[0]
            sortedOutput.append(self.data[currIndex])
        if sortedOutput is not None:
            self.displaySortedValues(sortedOutput)
        return "Error" 

    def binarySearch(self, index:int) -> int:
        low = 1 #skip headers
        high = len(self.data) - 1
        while low <= high:
            mid = (low + high) // 2
            if int(self.data[mid][0]) == index:
                return mid
            elif int(self.data[mid][0]) < index:
                low = mid + 1
            else:
                high = mid - 1
        return "Error"
    
    def displaySortedValues(self, arr:list) -> None:
        self.clearData()
        for row, rowData in enumerate(arr):
                for col, var in enumerate(rowData):
                    value_label = QLabel(var)
                    value_label.setAlignment(Qt.AlignCenter)

                    if var == "Win":
                        value_label.setStyleSheet("background-color: lightgreen; color: black;")
                    elif var == "Loss":
                        value_label.setStyleSheet("background-color: lightcoral; color: black;")
                    self.grid_layout.addWidget(value_label, row + 1, col)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)

    def headerClicked(self, v:str, button:QPushButton) -> None:
        if not self.firstHeaderPop: #meaning there is no data yet
            for element in self.headerButtons:
                # Reset all buttons to default dark purple
                element.setStyleSheet("background-color: #4B0082; color: white;")  # Lighter dark purple

            button.setStyleSheet("background-color: blue; color: white;")

            arr = self.createArr(v)
            sort = MySorting(index=self.indexClicked)
            sort.mergeSortTuples(arr, 0, len(arr) - 1)
            self.populateSortedValues(arr)

    def clearData(self) -> None:
        for i in reversed(range(self.main_layout.count(), 1)):
            item = self.main_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            else:
                self.main_layout.removeItem(item)
    
    def createArr(self, header:str) -> list:
        arr = []
        win = False
        if header == 'win':
            win = True
        
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)

            for row, rowData in enumerate(csv_reader):
                for col, var in enumerate(rowData):
                    if row == 0:
                        if var == header:
                            self.indexClicked = col
                    else:
                        if self.indexClicked is None:
                            return "Could not find specified header"
                        else:
                            if col == self.indexClicked:
                                if win:
                                    arr.append((row, self.stringToInt(var)))
                                else:
                                    arr.append((row, float(var)))
        return arr
    
    def stringToInt(self, element:str) -> int:
        if element == 'Win':
            return 1
        else:
            return 0