class GameStyle:
    def get_stylesheet(self) -> str:
        return """
            QWidget {
                background-color: #0a001a; /* Dark blue-purple background */
                font-family: Arial;
            }
            QLabel {
                color: #ffd700; /* Gold color for labels */
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #2e004d; /* Darker purple input background */
                color: white;
                font-size: 18px;
                padding: 5px;
                border: 1px solid #ffd700; /* Gold border */
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #ffd700;
            }
            QPushButton {
                background-color: #2e004d; /* Darker purple for buttons */
                color: #ffd700; /* Gold text for buttons */
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #ffd700;
            }
            QPushButton:hover {
                background-color: #3b0066; /* Lighter purple on hover */
                border-color: #ffd700;
            }
            QPushButton#startButton {
                background-color: #ffd700; /* Gold for start button */
                color: #0a001a; /* Dark blue-purple text */
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#startButton:hover {
                background-color: #ffe066; /* Lighter gold on hover */
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
                border: 1px solid #ffd700; /* Gold border for grid cells */
                border-radius: 5px;
                opacity: 1;
            }

            /* Top Horizontal Box */
            QFrame#topBar {
                background-color: #0a001a; /* Dark blue-purple for the top bar */
                border: 1px solid #ffd700; /* Gold border */
            }
            QLabel#topLabel {
                color: #ffd700;
                font-weight: bold;
            }

            /* Panel Styling */
            QWidget#controlPanel {
                background-color: #2e004d; /* Dark purple for control panel */
                border-radius: 10px;
                padding: 10px;
            }
        """
