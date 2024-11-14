""" Controls the grid of the game """

from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class GridLogic:
    def __init__(self, on_cell_click: callable) -> None:
        """ Defines the logic for the grid """
        self.grid_size = 5
        self.cells = {}  # Set of all cells in the grid. Each element is a tuple of (row, col)
        self.on_cell_click = on_cell_click  # function to call when a cell is clicked

    def setup_grid(self) -> QVBoxLayout:
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # Spacing between cells

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = QPushButton("")  # cell button
                cell.setMinimumSize(150, 150)
                cell.clicked.connect(lambda _, r=row, c=col: self.on_cell_click(r, c))
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                cell.setProperty("class", "grid-cell")
                cell.setIcon(QIcon("utils/imgs/cells/treasure.png"))
                cell.setIconSize(QSize(80, 80))


                # Apply a softer, modern gold border to each cell
                cell.setStyleSheet("""
                    QPushButton {
                        background-color: #444444;
                        border: 1px solid #C5A880;  /* Soft, modern gold border */
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #555555;
                        border-color: #B89B72;  /* Slightly muted gold on hover */
                    }
                    QPushButton:pressed {
                        background-color: #444444;
                        border-color: #C5A880;
                    }
                    QPushButton:disabled {
                        background-color: #444444;
                        color: #aaaaaa;
                        border-color: #C5A880;
                    }
                """)
                
                self.grid_layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return grid_container
        
    def disable_grid(self, disable: bool) -> None:
        """ Disables all buttons in the grid """
        for cell in self.cells.values(): # values are the respective buttons
            cell.setDisabled(disable)
        
    def disable_grid(self, disable: bool) -> None:
        for cell in self.cells.values(): # values are the respective buttons
            cell.setDisabled(disable)

    def reset_buttons(self) -> None:
        """ Reset the grid to its initial state for a new game"""

        for cell in self.cells.values():
            cell.setIcon(QIcon())  # Clear the icon
            cell.setEnabled(True)  # Enable to click on the cell
            cell.setStyleSheet("")  # Reset style to default version
            cell.setProperty("class", "grid-cell")  # Reapply the grid-cell class
            cell.setIcon(QIcon("utils/imgs/cells/treasure.png"))
            cell.setIconSize(QSize(80, 80))
            cell.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                border: 1px solid #C5A880;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #aaaaaa;
                border-color: #C5A880;
            }
        """)  # Fully reset style to ensure no gray overlay is retained


    def set_button_state(self, row: int, col: int, is_bomb: bool, revealed: bool = False) -> None:
        """ Changes the image and style of a cell accessing its buttons via its coordinates """
        cell = self.cells[(row, col)]  # Return the button at the given coordinates
        
        # Set the icon based on whether it's a bomb or a star
        if is_bomb:
            icon = QIcon("utils/imgs/cells/bomb.png")
        else:
            icon = QIcon("utils/imgs/cells/star.png")
        
        # Apply the icon and set the icon size explicitly
        cell.setIcon(icon)
        cell.setIconSize(QSize(80, 80))  # Keep the icon size consistent
        
        # Update the style to ensure no gray overlay or opacity is applied
        cell.setStyleSheet("""
            QPushButton {
                background-color: #444444;  /* Consistent background */
                border: 1px solid #FFCC00;  /* Bright gold border for contrast */
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #444444;  /* Ensure no overlay on disabled state */
                color: #FFFFFF;
            }
        """)

    def disable_button(self, row:int, col:int) -> None:
        self.cells[(row, col)].setDisabled(True)

    def reveal_cells(self, set_of_mines: set, clicked_cells: set) -> None:
        """ Reveals all cells that are not clicked"""
        # Showing all other mines
        non_clicked_cells = set(self.cells.keys()).difference(clicked_cells)
        # Revealing unclicked cells
        for row, col in non_clicked_cells:
            if (row, col) in set_of_mines:
                self.set_button_state(row, col, True, revealed=True)
            else:
                self.set_button_state(row, col, False, revealed=True)
