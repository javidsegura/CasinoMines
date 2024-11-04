""" Controls the data tab of the game """

from design.game_css import GameStyle
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QGridLayout)
from PySide6.QtCore import Qt
import csv

class DataTab(QWidget):
    def __init__(self, file_path:str="localVersion/utils/data/userData.csv") -> None:
        super().__init__()
        self.setStyleSheet(GameStyle().get_stylesheet())
        
        self.file_path = file_path
        self.data = []
        self.headerButtons = []
        self.firstHeaderPop = True

        self.mapping = {
            "id": "Game Number",
            "betAmount": "Bet Amount",
            "numMines": "Number of Mines",
            "balanceBefore": "Balance Before Game",
            "profit": "Profit",
            "balanceAfter": "Balance After Game",
            "win": "Win or Loss"
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
                        header_button.setCheckable(True)  # Optional: to make it behave like a toggle button
                        header_button.clicked.connect(lambda _, v=var, btn=header_button: self.headerClicked(v, btn))  # Connect to click event
                        if col == 0 and self.firstHeaderPop:
                            header_button.setStyleSheet("background-color: blue; color: white;")
                        self.grid_layout.addWidget(header_button, 0, col)
                        self.headerButtons.append(header_button)
    
    def populateValues(self) -> None:
        """ Populate the values of the data tab"""
        self.clearData()
        self.firstHeaderPop = False
        for i, element in enumerate(self.headerButtons):
            if i == 0:
                element.setStyleSheet("background-color: blue; color: white;")
            else:
                element.setStyleSheet("background-color: #444444; color: white;")

        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            self.data = []
            self.data = list(csv_reader) #each time something is added to userData, self.data updates
            for row, rowData in enumerate(self.data):
                for col, var in enumerate(rowData):
                    if not row == 0:
                        value_label = QLabel(str(var))
                        value_label.setAlignment(Qt.AlignCenter)

                        if str(var) == "Win":
                            value_label.setStyleSheet("background-color: lightgreen; color: black;")
                        elif str(var) == "Loss":
                            value_label.setStyleSheet("background-color: lightcoral; color: black;")
                        self.grid_layout.addWidget(value_label, row, col)
        
        # self.main_layout.addLayout(self.grid_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)


    
    def populateSortedValues(self, arr:list) -> None:
        sortedOutput = []
        for element in arr:
            currIndex = element[0]
            # binary search
            sortedOutput.append(self.data[self.binarySearch(currIndex)])
        if sortedOutput is not None:
            #print(f"SortedOutput {sortedOutput}\n")
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
                element.setStyleSheet("background-color: #444444; color: white;")

            #print(f"\nHeader {v} has been clicked")
            button.setStyleSheet("background-color: blue; color: white;")

            arr = self.createArr(v)
            #print(f"Arr unsorted: {arr}")
            sorted = self.mergeSort(arr, 0, len(arr) - 1)
            #print(f"Arr sorted: {sorted}")
            self.populateSortedValues(sorted)

    def clearData(self) -> None:
        # self.headerButtons = []
        for i in reversed(range(self.main_layout.count(), 1)):
            item = self.main_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            else:
                self.main_layout.removeItem(item)
    
    def createArr(self, header:str) -> list:
        arr = []
        ourCol = None
        win = False
        if header == 'win':
            win = True
        
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)

            for row, rowData in enumerate(csv_reader):
                for col, var in enumerate(rowData):
                    if row == 0:
                        if var == header:
                            ourCol = col
                    else:
                        if ourCol is None:
                            return "Could not find specified header"
                        else:
                            if col == ourCol:
                                if win:
                                    arr.append((row, self.stringToInt(var)))
                                else:
                                    arr.append((row, float(var)))
        return arr
    
    def stringToInt(self, element:str) -> int:
        # only for win as of right now
        if element == 'Win':
            return 1
        else:
            return 0

    def merge(self, arr:list, start:int, mid:int, end:int) -> None:
        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]

        i = j = 0
        k = start

        # Merge the two halves
        while i < len(left) and j < len(right):
            if left[i][1] <= right[j][1]:  # Compare based on second element of tuple
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        # Copy any remaining elements from the left half
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        # Copy any remaining elements from the right half
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    
    def mergeSort(self, arr:list, start:int, end:int) -> list:
        if start < end:
            mid = (start + end) // 2

            # Recursively split and sort both halves
            self.mergeSort(arr, start, mid)
            self.mergeSort(arr, mid + 1, end)

            # Merge the sorted halves
            self.merge(arr, start, mid, end)
        return arr
