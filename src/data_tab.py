from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame, QMessageBox, QTabWidget, QGridLayout)
from PySide6.QtCore import Qt
import csv

class DataTab(QWidget):
    def __init__(self, file_path="utils/data/userData.csv"):
        super().__init__()
        
        self.file_path = file_path

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
    

    def populateHeaders(self):
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for i, row in enumerate(csv_reader):
                for col, var in enumerate(row):
                    if i == 0:
                        header_button = QPushButton(self.mapping[var])  # Use QPushButton
                        header_button.setCheckable(True)  # Optional: to make it behave like a toggle button
                        header_button.clicked.connect(lambda _, v=var: self.headerClicked(v))  # Connect to click event
                        self.grid_layout.addWidget(header_button, 0, col)
    
    def populateValues(self):
        self.clearData()
        self.populateHeaders()

        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for row, rowData in enumerate(csv_reader):
                for col, var in enumerate(rowData):
                    if not row == 0:
                        value_label = QLabel(str(var))
                        value_label.setAlignment(Qt.AlignCenter)

                        if str(var) == "Win":
                            value_label.setStyleSheet("background-color: lightgreen; color: black;")
                        elif str(var) == "Loss":
                            value_label.setStyleSheet("background-color: red; color: black;")
                        self.grid_layout.addWidget(value_label, row, col)
        
        self.main_layout.addLayout(self.grid_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)

        # data sorting testing
        header = 'profit'
        arr = self.createArr(header)
        print(f"Arr float: {arr}")
        sorted = self.mergeSort(arr, 0, len(arr) - 1)
        print(f"Arr sorted: {sorted}")

    def headerClicked(self, v):
        print(f"Header {v} has been clicked")

    def clearData(self):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            else:
                self.main_layout.removeItem(item)
    
    def createArr(self, header):
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
                            ourCol = col
                    else:
                        if not ourCol:
                            return "Could not find specified header"
                        else:
                            if col == ourCol:
                                if win:
                                    arr.append((row, self.stringToInt(var)))
                                else:
                                    arr.append((row, float(var)))
        return arr
    
    def stringToInt(self, element):
        # only for win as of right now
        # win = 1
        # loss = 0
        if element == 'Win':
            return 1
        else:
            return 0

    def merge(self, arr, start, mid, end):
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
    
    def mergeSort(self, arr, start, end):
        if start < end:
            mid = (start + end) // 2

            # Recursively split and sort both halves
            self.mergeSort(arr, start, mid)
            self.mergeSort(arr, mid + 1, end)

            # Merge the sorted halves
            self.merge(arr, start, mid, end)
        return arr
