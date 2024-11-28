""" Controls the data tab of the game """

from others.algorithms.sorting import MySorting
from design.game_css import GameStyle
from PySide6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel,
                                QSpacerItem, QSizePolicy, QGridLayout)
from PySide6.QtCore import Qt
import csv


class DataTab(QWidget):
    def __init__(self, file_path:str="./utils/data/game_stats.csv") -> None:
        """ Initilaizes the game stats Tab
        Time Complexity:
            - O(n^m): where n is the number of rows in the CSV file and m is the number of columns in the CSV file
        """
        super().__init__()
        self.setStyleSheet(GameStyle().get_stylesheet())
        
        self.file_path = file_path
        self.data = []
        self.headerButtons = []
        self.firstHeaderPop = True

        self.mapping = {
            "win": "Win",
            "gameId": "Game ID",
            "betAmount": "Bet Amount",
            "numMines": "Number of Mines",
            "balanceBefore": "Balance Before",
            "balanceAfter": "Balance After",
            "profit": "Profit"
        }
        # gameId,win,betAmount,numMines,balanceBefore,balanceAfter,profit
        self.stringToIndex = {
            "gameId": 0,
            "win": 1,
            "betAmount": 2,
            "numMines": 3,
            "balanceBefore": 4,
            "balanceAfter": 5,
            "profit": 6
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
    
    def populateHeaders(self) -> None:
        """ Populate the headers with clickable buttons for sorting
        Time Complexity:
            - O(n^m): where n is the number of rows in the CSV file and m is the number of columns in the CSV file
        """
        self.headerButtons = []
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for i, row in enumerate(csv_reader):
                for col, var in enumerate(row):
                    if i == 0:
                        header_button = QPushButton(self.mapping[var]) 
                        header_button.setCheckable(True)
                        header_button.clicked.connect(lambda _, v=var, btn=header_button: self.headerClicked(v, btn))

                        # Set default dark purple for all header buttons
                        header_button.setStyleSheet("background-color: #5A3D8A; color: white;") 
                        self.grid_layout.addWidget(header_button, 0, col)
                        self.headerButtons.append(header_button)

    def populateGameStats(self) -> None:
        """ Populate the values of the data tab
        Time Complexity:
            - O(n*m): where n is the number of rows in the CSV file and m is the number of elements being deleted from main_layout
        """
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

                        if str(var) == "Win":
                            value_label.setStyleSheet("background-color: lightgreen; color: black;")
                        elif str(var) == "Loss":
                            value_label.setStyleSheet("background-color: lightcoral; color: black;")
                        self.grid_layout.addWidget(value_label, row, col)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)
    
    def populateSortedValues(self, arr:list) -> None:
        """ Receives a sorted list of tuples representing it's index in self.data 
            and appends each row to a new list in order
        Time Complexity:
            - O(n^2): where n is the number of rows in the CSV file
            - O(n): when appending is amortized to constant time
        """
        # sortedOutput = []
        # for element in arr:
        #     currIndex = element[0]
        #     sortedOutput.append(self.data[currIndex]) # 
        if arr is not None:
            self.displaySortedValues(arr)
        return "Error" 

    def displaySortedValues(self, arr:list) -> None:
        """ Displays a sorted list
        Time Complexity:
            - O(n^2): where n is the number of rows in the CSV file
        """
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
        """ Describes process when a user has clicked on a head button
        Time Complexity:
            - O(n * log n): where n is the number of rows in the CSV file
        Merge sort dominates time complexity here.
        """
        if not self.firstHeaderPop:  # Check if data is already displayed
            for element in self.headerButtons:
                # Reset all buttons to default dark purple
                element.setStyleSheet("background-color: #4B0082; color: white;")

            # Set the clicked button to a darker purple
            button.setStyleSheet("background-color: #2E0854; color: white;")
            
            # arr = self.createArr(v)
            print(f"Index: {self.stringToIndex[v]}")
            sorted = self.data[1:] #Exclude headers
            print(sorted)
            MySorting(self.stringToIndex[v], ascending=False).mergeSort(sorted, 0, len(sorted)) # O(n * log n) 
            print(sorted)
            #sorted = self.mergeSort(arr, 0, len(arr) - 1)
            self.populateSortedValues(sorted)

    def clearData(self) -> None:
        """ Iterates through all elements on the tab and deletes them
        Time Complexity:
            - O(n): where n is the number of elements in main_layout
        """
        for i in reversed(range(self.main_layout.count(), 1)):
            item = self.main_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            else:
                self.main_layout.removeItem(item)
    
    def createArr(self, header:str) -> list:
        """ Creates an array of tuples according to clicked header
        Time Complexity:
            - O(n^2): where n is the number of rows in the CSV file
        """
        arr = []
        win = False
        ourCol = None
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
        """ Converts the boolean values representing win or loss to text
        Time Complexity:
            - O(1): All operations run in constant time
        """
        if element == 'Win':
            return 1
        else:
            return 0

    def merge(self, arr, start, mid, end):
        """ Merge component of merge sort
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
        Where n is the number of elements between start and end
        """ 
        # Start indexes for the two halves
        left_index = start
        right_index = mid + 1

        # Iterate over the array and merge in place
        while left_index <= mid and right_index <= end:
            # If the left element is in the right place, move on
            if arr[left_index][1] <= arr[right_index][1]:
                left_index += 1
            else:
            # Right element is smaller, so we need to insert it before the left element
                value = arr[right_index]
                index = right_index

                # Shift all elements between left_index and right_index to the right
                while index > left_index:
                    arr[index] = arr[index - 1]
                    index -= 1

                arr[left_index] = value

                # Update all indexes, including mid since we shifted the elements
                left_index += 1
                right_index += 1
                mid += 1
    
    def mergeSort(self, arr, start, end): # **sorts from smallest --> largest**
        """ Merge sort implementation for a list of tuples
        Time Complexity:
            Worst Case: O(n log n)
            Avg Case: O(n log n)
        Where n is the number of elements in arr
        """
        if start < end:
            mid = (start + end) // 2

            # Recursively split and sort both halves
            self.mergeSort(arr, start, mid)
            self.mergeSort(arr, mid + 1, end)

            # Merge the sorted halves
            self.merge(arr, start, mid, end)
        return arr