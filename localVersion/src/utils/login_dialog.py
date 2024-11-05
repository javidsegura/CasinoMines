from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame)
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor, QFont, QPalette, QBrush
from PySide6.QtCore import Qt, QPoint, QTimer

class ShimmerButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.shimmer_pos = 0
        
        # Setup animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_shimmer)
        self.timer.start(50)  # Update every 50ms
        
    def update_shimmer(self):
        self.shimmer_pos = (self.shimmer_pos + 10) % (self.width() + 200)
        self.update()
        
    def paintEvent(self, event):
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to CasinoMines!")
        self.setFixedSize(400, 300)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("CASINO MINES")
        title.setFixedHeight(80)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(50)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #FFD700;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.2);
                color: white;
                font-size: 18px;
            }
            QLineEdit:focus {
                border: 2px solid #FFA500;
            }
        """)
        layout.addWidget(self.username_input)

        # Login button with shimmer effect
        self.login_button = ShimmerButton("START PLAYING")
        self.login_button.setFixedHeight(60)
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #FFD700, stop:1 #FFA500);
                border: none;
                border-radius: 10px;
                color: black;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #FFA500, stop:1 #FF4500);
            }
        """)
        layout.addWidget(self.login_button)
        
        layout.addStretch()
        
        # Set dialog background
        self.setStyleSheet("""
            QDialog {
                background-image: url(localVersion/utils/imgs/login_bg.jpg);
                background-position: center;
                background-repeat: no-repeat;
                background-color: rgba(0, 0, 0, 0.8);
                border-radius: 15px;
            }
        """)
        
        self.login_button.clicked.connect(self.accept)

    def get_username(self):
        return self.username_input.text().strip()

def show_login_dialog(parent=None) -> str:
    """Show login dialog and return username"""
    while True:
        dialog = LoginDialog(parent)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            username = dialog.get_username()
            if username and username.isalnum():
                return username