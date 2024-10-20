from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
                                QLineEdit, QSpacerItem, QSizePolicy, QSlider, QFrame, QMessageBox, QTabWidget, QGridLayout)
from PySide6.QtCore import Qt
import csv

class DataTab(QWidget):
    def __init__(self, file_path="utils/data/userData.csv"):
        super().__init__()
        
        self.file_path = file_path

        self.mapping = {
            "id": "ID",
            "betAmount": "Bet Amount",
            "numMines": "Number of Mines",
            "balanceBefore": "Balance Before Game",
            "profit": "Profit",
            "balanceAfter": "Balance After Game"
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
                        header_label = QLabel(f"<b>{self.mapping[var]}<b>")
                        self.grid_layout.addWidget(header_label, 0, col)
    
    def populateValues(self):
        self.clearData()
        self.populateHeaders()

        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for row, rowData in enumerate(csv_reader):
                for col, var in enumerate(rowData):
                    if not row == 0:
                        value_label = QLabel(str(var))
                        self.grid_layout.addWidget(value_label, row, col)
        
        self.main_layout.addLayout(self.grid_layout)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addItem(spacer)
        self.setLayout(self.main_layout)

    def clearData(self):
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            else:
                self.main_layout.removeItem(item)
