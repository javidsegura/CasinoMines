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
                cell.setFlat(True)  # Disable default shading and overlay effect
                cell.clicked.connect(lambda _, r=row, c=col: self.on_cell_click(r, c))
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                cell.setProperty("class", "grid-cell")
                cell.setIcon(QIcon("utils/imgs/cells/diamond.png"))
                cell.setIconSize(QSize(80, 80))

                # Set background color and border styling to match the reference
                cell.setStyleSheet("""
                    QPushButton {
                        background-color: #2b1d39;  /* Dark purple background */
                        border: 1px solid #3e2c53;  /* Subtle purple border */
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #3a2a4f;  /* Slightly lighter purple on hover */
                    }
                    QPushButton:pressed {
                        background-color: #2b1d39;
                        border: 2px solid #ffd700;  /* Gold border when clicked */
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
            cell.setIcon(QIcon("utils/imgs/cells/diamond.png"))
            cell.setIconSize(QSize(80, 80))
            cell.setStyleSheet("""
            QPushButton {
                background-color: #2b1d39;
                border: 1px solid #C5A880;
                border-radius: 5px;
            }
            QPushButton:disabled {
                background-color: #2b1d39;
                color: #aaaaaa;
                border-color: #C5A880;
            }
        """)  # Fully reset style to ensure no gray overlay is retained


    def set_button_state(self, row: int, col: int, is_bomb: bool, revealed: bool = False) -> None:
        """Changes the image and style of a cell, ensuring immediate icon update with transparent background."""
        cell = self.cells[(row, col)]
        
        # Set the icon based on whether it's a bomb or a star
        icon = QIcon("utils/imgs/cells/bomb.png") if is_bomb else QIcon("utils/imgs/cells/coin.png")
        cell.setIcon(icon)
        
        # Dynamically set icon size relative to cell size
        cell_size = min(cell.width(), cell.height()) * 0.8
        cell.setIconSize(QSize(cell_size, cell_size))
        
        # Style for revealed and non-revealed cells with transparent background
        if revealed:
            # Styling for unclicked cells with subtle gold border
            cell.setStyleSheet("""
                QPushButton {
                    background-color: #2b1d39;  /* Transparent background */
                    border: 0.5px solid #B89B72;  /* Subtle gold border for unclicked cells */
                    border-radius: 3px;
                }
            """)
            cell.setDisabled(True)  # Disable the button once revealed
        else:
            # Styling for clicked cells with strong gold border
            cell.setStyleSheet("""
                QPushButton {
                    background-color: transparent;  /* Transparent to show underlying purple */
                    border: 3.5px solid #FFCC00;  /* Bright gold border for clicked cells */
                    border-radius: 3px;
                }
            """)
        
        # Immediate repaint to ensure the icon and style are updated
        cell.repaint()



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