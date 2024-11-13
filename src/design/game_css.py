class GameStyle:
    def get_stylesheet(self) -> str:
        return """
            QWidget {
                background-color: #00001a; /* Darker navy blue, almost black */
                font-family: Arial;
            }
            QLabel {
                color: #ffcc00; /* Match "Confirm Selection" button color */
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #444444;
                color: white;
                font-size: 18px;
                padding: 5px;
                border: 1px solid #ffcc00;  /* Match "Confirm Selection" button color */
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #ffcc00;
            }
            QPushButton {
                background-color: #444444;
                color: #ffcc00; /* Match "Confirm Selection" button color */
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #ffcc00;
            }
            QPushButton:hover {
                background-color: #555555;
                border-color: #ffcc00;
            }
            QPushButton#startButton {
                background-color: #ffcc00;
                color: black;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#startButton:hover {
                background-color: #ffd633; /* Slightly lighter shade */
            }
            QPushButton#startButton:disabled {
                background-color: #888888;
                color: #aaaaaa;
            }
            QPushButton:disabled {
                background-color: #888888;
                color: #aaaaaa;
            }
            
            /* Grid Cell Specific Styling */
            QPushButton#grid-cell {
                background-color: transparent;
                border: 1px solid #ffcc00;  /* Match "Confirm Selection" button color */
                border-radius: 5px;
                opacity: 1;
            }

            /* Top Horizontal Box */
            QFrame#topBar {
                background-color: #00001a; /* Darker navy blue for the top bar as well */
                border: 1px solid #ffcc00; /* Subtle border to match "Confirm Selection" */
            }
            QLabel#topLabel {
                color: #ffcc00;
                font-weight: bold;
            }
        """
