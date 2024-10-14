
class GameStyle:
    def __init__(self):
        None
    def get_stylesheet(self):
        """
        Def: sets CSS for UI widgets
        Question: which widget is which? 
        """
        return """
            QWidget {
                background-color: #2b2b2b;
                font-family: Arial;
            }
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            QLineEdit {
                background-color: #444444;
                color: white;
                font-size: 18px;
                padding: 5px;
                border: 2px solid #555555;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border-color: #ffcc00;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton#startButton {
                background-color: #ffcc00;
                color: black;
                font-size: 18px;
            }
            QPushButton#startButton:hover {
                background-color: #ffd633;
            }
            QPushButton:disabled {
                background-color: #888888;
                color: #aaaaaa;
            }
            QPushButton.grid-cell {
                border-radius: 10px;
            }
        """

