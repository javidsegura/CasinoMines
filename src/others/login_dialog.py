from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame)
from PySide6.QtGui import QPixmap, QPainter, QLinearGradient, QColor
from PySide6.QtCore import Qt, QTimer

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
    def __init__(self, parent=None, err=None):
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
        title = QLabel("Welcome to CasinoMines!")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 30px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setFixedHeight(50)
        self.username_input.setFixedWidth(400)  # Fixed width for better appearance
        if err is not None:
            self.username_input.setPlaceholderText(err)
        else:
            self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #000000;
                border-radius: 10px;
                background: rgba(255, 255, 255, 0.3);
                color: white;
                font-size: 20px;
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
                                          stop:0 #FFD700, stop:1 #FFA500);
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                font-size: 17px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #FFA500, stop:1 #FF4500);
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

    def get_username(self):
        return self.username_input.text().strip().lower()


def show_login_dialog(parent=None, err=None) -> str:
    """Show login dialog and return username"""
    while True:
        dialog = LoginDialog(parent, err)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            username = dialog.get_username()
            if username and username.isalnum():
                return str(username)