""" Controls the grid of the game """

from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class GridLogic:
    def __init__(self, on_cell_click: callable) -> None:
        """
        Initializes the logic for the grid.
        :param on_cell_click: A callable function that will be invoked when a cell is clicked.
        Time Complexity:
            Worst Case: O(1) - Initializing variables and an empty dictionary.
            Avg Case: O(1)
        """
        self.grid_size = 5  # Defines the grid dimensions (5x5 grid by default).
        self.cells = {}  # Dictionary to store all grid cells, with keys as (row, col).
        self.on_cell_click = on_cell_click  # Stores the callback function for cell clicks.

    def setup_grid(self) -> QVBoxLayout:
        """
        Creates and sets up the game grid layout.
        :return: A QVBoxLayout containing the grid and spacers for alignment.
        Time Complexity:
            Worst Case: O(grid_size^2) - Iterates through all rows and columns of the grid to create buttons.
            Avg Case: O(grid_size^2)
        """
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # Adds spacing between cells.

        # Loop through the rows and columns to create the grid cells.
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Create a QPushButton to represent a grid cell.
                cell = QPushButton("")
                cell.setMinimumSize(150, 150)  # Set minimum cell size.
                cell.setFlat(True)  # Remove shading effects on the button.
                cell.clicked.connect(lambda _, r=row, c=col: self.on_cell_click(r, c))  # Connect the cell click signal.
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Ensure cells expand in the layout.
                cell.setProperty("class", "grid-cell")  # Assign a class property for styling.
                cell.setIcon(QIcon("utils/imgs/cells/diamond.png"))  # Set the default icon.
                cell.setIconSize(QSize(80, 80))  # Set the default icon size.

                # Define the cell's styling for normal, hover, and clicked states.
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

                # Add the cell to the grid layout and store it in the dictionary.
                self.grid_layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

        # Create a vertical layout to contain the grid with spacers for alignment.
        grid_container = QVBoxLayout()
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        grid_container.addLayout(self.grid_layout)
        grid_container.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return grid_container

    def disable_grid(self, disable: bool) -> None:
        """
        Disables or enables all buttons in the grid.
        :param disable: A boolean indicating whether to disable (True) or enable (False) the grid.
        Time Complexity:
            Worst Case: O(grid_size^2) - Iterates through all buttons in the grid.
            Avg Case: O(grid_size^2)
        """
        for cell in self.cells.values():  # Iterate through all cells in the grid.
            cell.setDisabled(disable)

    def reset_buttons(self) -> None:
        """
        Resets all buttons in the grid to their initial state for a new game.
        Time Complexity:
            Worst Case: O(grid_size^2) - Iterates through all buttons in the grid to reset them.
            Avg Case: O(grid_size^2)
        """
        for cell in self.cells.values():
            cell.setIcon(QIcon())  # Clear the cell's icon.
            cell.setEnabled(True)  # Re-enable the cell.
            cell.setStyleSheet("")  # Clear any custom styles applied during gameplay.
            cell.setProperty("class", "grid-cell")  # Reapply the class property.
            cell.setIcon(QIcon("utils/imgs/cells/diamond.png"))  # Reset the default icon.
            cell.setIconSize(QSize(80, 80))  # Reset the default icon size.
            # Reapply the default styling for the cell.
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
        """)

    def set_button_state(self, row: int, col: int, is_bomb: bool, revealed: bool = False) -> None:
        """
        Changes the state of a specific button in the grid.
        :param row: The row index of the button.
        :param col: The column index of the button.
        :param is_bomb: A boolean indicating whether the button represents a bomb.
        :param revealed: A boolean indicating whether the button is revealed or clicked.
        Time Complexity:
            Worst Case: O(1) - Accessing a specific button and updating its properties.
            Avg Case: O(1)
        """
        cell = self.cells[(row, col)]  # Get the cell at the specified row and column.

        # Set the icon based on whether it's a bomb or a coin.
        icon = QIcon("utils/imgs/cells/bomb.png") if is_bomb else QIcon("utils/imgs/cells/coin.png")
        cell.setIcon(icon)

        # Dynamically adjust the icon size based on the cell's dimensions.
        cell_size = min(cell.width(), cell.height()) * 0.8
        cell.setIconSize(QSize(cell_size, cell_size))

        # Apply the appropriate styles for revealed and non-revealed cells.
        if revealed:
            cell.setStyleSheet("""
                QPushButton {
                    background-color: #2b1d39;
                    border: 0.5px solid #B89B72;
                    border-radius: 3px;
                }
            """)
            cell.setDisabled(True)  # Disable the button once it is revealed.
        else:
            cell.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 3.5px solid #FFCC00;
                    border-radius: 3px;
                }
            """)

        cell.repaint()  # Immediately repaint to update the button's appearance.

    def disable_button(self, row: int, col: int) -> None:
        """
        Disables a specific button in the grid.
        :param row: The row index of the button.
        :param col: The column index of the button.
        Time Complexity:
            Worst Case: O(1) - Direct access and operation on a specific button.
            Avg Case: O(1)
        """
        self.cells[(row, col)].setDisabled(True)

    def reveal_cells(self, set_of_mines: set, clicked_cells: set) -> None:
        """
        Reveals all cells that are not clicked.
        :param set_of_mines: A set of (row, col) tuples representing the positions of mines.
        :param clicked_cells: A set of (row, col) tuples representing the clicked cells.
        Time Complexity:
            Worst Case: O(grid_size^2) - Iterates through all cells in the grid.
            Avg Case: O(n), where n is the number of unclicked cells.
        """
        # Identify all non-clicked cells.
        non_clicked_cells = set(self.cells.keys()).difference(clicked_cells)

        # Reveal each non-clicked cell.
        for row, col in non_clicked_cells:
            if (row, col) in set_of_mines:
                self.set_button_state(row, col, True, revealed=True)
            else:
                self.set_button_state(row, col, False, revealed=True)
