from board.settings import Settings

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QInputDialog
from PySide6.QtCore import Slot

class PayoutTab(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add money button
        add_money_button = QPushButton("Add Money")
        add_money_button.clicked.connect(self.add_money)
        layout.addWidget(add_money_button)

        # Check out money button
        check_out_button = QPushButton("Check Out Money")
        check_out_button.clicked.connect(self.check_out_money)
        layout.addWidget(check_out_button)

        self.setLayout(layout)

    def add_money(self):
        amount, ok = QInputDialog.getDouble(self, "Add Money", "Enter amount to add:", 0, 0, 10000, 2)
        if ok:
            # Assuming settings has an add_balance method
            self.settings.increase_balance(amount)

    def check_out_money(self):
        amount, ok = QInputDialog.getDouble(self, "Check Out Money", "Enter amount to check out:", 0, 0, 10000, 2)
        if ok:
            self.settings.increase_balance(-amount)
      
