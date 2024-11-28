""" Controls the grid of the game """

from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class GridLogic:
    def __init__(self, on_cell_click: callable) -> None:
        """ Defines the logic for the grid 
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.grid_size = 5
        self.cells = {}  # Set of all cells in the grid. Each element is a tuple of (row, col)
        self.on_cell_click = on_cell_click  # function to call when a cell is clicked

    def setup_grid(self) -> QVBoxLayout:
        """
        Description: sets up the grid
        Time Complexity:
            - Worst case: O(n^3): where n*n is the size of the grid and the third n is given because
                 of a very poor hashing function that makes the dictionary insertions collide every time
            - Average case: O(n^2): where n*n is the size of the grid and when inserting in a set of cells that 
                are not bombs and the dictionary has a good hashing function
        """
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
                self.cells[(row, col)] = cell # coordinates:button object

        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return grid_container


        
    def disable_grid(self, disable: bool) -> None:
        """ Description: Disables all buttons in the grid
        Time Complexity:
            - O(n): where n is the number of cells in the grid. Note this is pure asymptotic analysis. This ignores the fact that for
                our game we have fixed the maximum number of cells to 25.
        """
        for cell in self.cells.values(): # values are the respective buttons objects 
            cell.setDisabled(disable)
        
    def disable_grid(self, disable: bool) -> None:
        """ Description: Disables all buttons in the grid
        Time Complexity:
            - O(n): where n is the number of cells in the grid. Note this is pure asymptotic analysis. This ignores the fact that for
                our game we have fixed the maximum number of cells to 25.
        """
        for cell in self.cells.values(): # values are the respective buttons
            cell.setDisabled(disable)

    def reset_buttons(self) -> None:
        """ Description: Reset the grid to its initial state for a new game
        Time Complexity:
            - O(n): where n is the number of cells in the grid. Note this is pure asymptotic analysis. This ignores the fact that for
                our game we have fixed the maximum number of cells to 25.
        """
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
        """ Description: Changes the image and style of a cell, ensuring immediate icon update with transparent background.
        Time Complexity:
            - Average case: O(1): retrieving value in self.cells dictionary is O(1)
            - Worst case: O(n): retrieving value in self.cells dictionary is O(n) because of a very poor hashing function
        """
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
        """ Description: Disables a specific button in the grid
        Time Complexity:
            - Average case: O(1): retrieving value in self.cells dictionary is O(1)
            - Worst case: O(n): retrieving value in self.cells dictionary is O(n) because of a very poor hashing function
        """
        self.cells[(row, col)].setDisabled(True)


    def reveal_cells(self, set_of_mines: set, clicked_cells: set) -> None:
        """ Description: Reveals all cells that are not clicked
        Time Complexity:
            - Average case: O(n): where n is the number of cells in the grid. Note this is pure asymptotic analysis. This ignores the fact that for
                our game we have fixed the maximum number of cells to 25.
            - Worst case: O(n^2): where n is the number of cells in the grid. The second n comes from having a very poor hashing when checking
                if present (row, col) in set_of_mines
        """
        non_clicked_cells = set(self.cells.keys()).difference(clicked_cells) # set theory. This takes O(n) time. Returns the key cells are not clicked
        # Revealing unclicked cells
        for row, col in non_clicked_cells: # O(n) too
            if (row, col) in set_of_mines: # O(1) / O(n)
                self.set_button_state(row, col, True, revealed=True)
            else:
                self.set_button_state(row, col, False, revealed=True)