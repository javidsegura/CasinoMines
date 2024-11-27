class GameStyle:
    def get_stylesheet(self) -> str:
        return """
            QWidget {
                background-color: #0a001a; /* Dark blue-purple background */
                font-family: Arial;
            }
            QLabel {
                color: #c1cdcd; /* Gold color for labels */
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #2e004d; /* Darker purple input background */
                color: white;
                font-size: 18px;
                padding: 5px;
                border: 1px solid #c1cdcd; /* Gold border */
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #c1cdcd;
            }
            QPushButton {
                background-color: #2e004d; /* Dark purple for buttons */
                color: #c1cdcd; /* Gold text for buttons */
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #c1cdcd;
            }
            QPushButton:hover {
                background-color: #3b0066; /* Lighter purple on hover */
                border-color: #c1cdcd;
            }
            QPushButton#startButton {
                background-color: #c1cdcd; /* Gold for start button */
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
                background-color: #3b0066; /* Dark purple for disabled state to match game theme */
                color: #aaaaaa;
            }

            /* Grid Cell Specific Styling */
            QPushButton#grid-cell {
                background-color: #4B0082; /* Dark purple background for grid cells */
                border: 1px solid #c1cdcd; /* Gold border for grid cells */
                border-radius: 5px;
                opacity: 1;
            }

            /* Top Horizontal Box */
            QFrame#topBar {
                background-color: #0a001a; /* Dark blue-purple for the top bar */
                border: 1px solid #c1cdcd; /* Gold border */
            }
            QLabel#topLabel {
                color: #c1cdcd;
                font-weight: bold;
            }

            /* Panel Styling */
            QWidget#controlPanel {
                background-color: #2e004d; /* Dark purple for control panel */
                border-radius: 10px;
                padding: 10px;
            }
        """
