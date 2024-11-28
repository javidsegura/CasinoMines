
import pandas as pd

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame)
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QFontDatabase
from PySide6.QtCore import Qt, QTimer


class ShimmerButton(QPushButton):
    def __init__(self, text:str, parent=None) -> None:
        """
        Description: initializes the ShimmerButton class
        Time Complexity:
            - O(1): All operations run in constant time
        """
        super().__init__(text, parent)
        self.shimmer_pos = 0
        
        # Setup animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_shimmer)
        self.timer.start(50)  # Update every 50ms
    
    def update_shimmer(self) -> None:
        """
        Description: updates the shimmer
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.shimmer_pos = (self.shimmer_pos + 10) % (self.width() + 200)
        self.update()

    def paintEvent(self, event) -> None:
        """
        Description: paints the event
        Time Complexity:
            - O(1): All operations run in constant time
        """
        super().paintEvent(event)
        painter = QPainter(self)
        
        # Create shimmer gradient
        gradient = QLinearGradient(
            self.shimmer_pos - 100, 0,
            self.shimmer_pos + 100, 0
        )
        gradient.setColorAt(0, QColor(255, 255, 255, 0))
        gradient.setColorAt(0.5, QColor(255, 255, 255, 100))
        gradient.setColorAt(1, QColor(255, 255, 255, 0))
        
        painter.fillRect(0, 0, self.width(), self.height(), gradient)

class LoginDialog(QDialog):
    def __init__(self, parent=None) -> None:
        """
        Description: initializes the LoginDialog class
        Time Complexity:
            - O(1): All operations run in constant time
        """
        super().__init__(parent)
        self.setWindowTitle("Log-in")
        self.setFixedSize(1000, 600)

        self.setStyleSheet("""
            QDialog {
                background-image: url(./utils/imgs/log_in.png);
                background-position: center;
                background-repeat: no-repeat;
            }
            QFrame {
                background: transparent;
            }
        """)
        
        # Main layout changed to horizontal
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Left panel container
        left_panel = QFrame()
        left_panel.setFixedWidth(self.width() // 2)
        left_panel.setStyleSheet("background: rgba(0, 0, 0, 0);")  # Semi-transparent black background
        left_layout = QVBoxLayout(left_panel)

        # Add stretch to push content to center vertically
        left_layout.addStretch()

        # Title
        font_id = QFontDatabase.addApplicationFont("./utils/fonts/ZenDots-Regular.ttf")
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Default"  # Fallback if the font fails to load
        title = QLabel("Welcome to CasinoMines")
        title.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-family: '{font_family}';
                font-size: 35px;
                font-weight: bold;
            }}
        """)
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # Add description below the title
        description = QLabel("Experience the thrill of the game!")
        description.setStyleSheet("""
            QLabel {
                color: #cecece; /* A light gray */
                font-size: 14px;
                font-style: italic;
                padding-bottom: 5px;
            }
        """)
        description.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(description)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(50)
        self.username_input.setFixedWidth(400)  # Fixed width for better appearance
        self.username_input.setPlaceholderText("Your username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #000000;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.3);
                color: white;
                font-size: 17px;
            }
            QLineEdit:focus {
                border: 2px solid #666666;
            }
        """)
        left_layout.addWidget(self.username_input, 0, Qt.AlignCenter)

        # Login button with shimmer effect
        self.login_button = ShimmerButton("Start Playing")
        self.login_button.setFixedHeight(60)
        self.login_button.setFixedWidth(400)  # Match input width
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #4B0082, stop:1 #9370DB);
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                            stop:0 #6A0DAD, stop:1 #D8BFD8);
            }

        """)
        left_layout.addWidget(self.login_button, 0, Qt.AlignCenter)

        # Add stretch to push content to center vertically
        left_layout.addStretch()

        # Right panel (transparent)
        right_panel = QFrame()
        right_panel.setFixedWidth(self.width() // 2)
        right_panel.setStyleSheet("background: transparent;")

        # Add image to right panel
        right_layout = QVBoxLayout(right_panel)
        image_label = QLabel()
        pixmap = QPixmap("./utils/imgs/gambling_icon.png")  # Replace with your image path
        
        scaled_pixmap = pixmap.scaled(550, 550, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(image_label)

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
        self.login_button.clicked.connect(self.accept)

    def get_username(self) -> str:
        """
        Description: gets the username
        Time Complexity:
            - O(n): where n is the length of the username string. This is because you have to iterate through the string, check for separator and append to array
        """
        return self.username_input.text().strip()

def show_login_dialog(parent=None) -> str:
    """
    Description: shows the login dialog and returns the username
    Time Complexity:
        - Does not apply (it depends on the number of times it takes for the user to input a valid username; usually O(1))
    """
    while True:
        dialog = LoginDialog(parent)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            username = dialog.get_username()
            if username and username.isalnum():
                return str(username)