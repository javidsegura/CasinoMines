from PySide6.QtWidgets import QPushButton, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class GridLogic:
    def __init__(self, on_cell_click : callable) -> None:
        """ Defines the logic for the grid """
        self.grid_size = 5
        self.cells = {} # Set of all cells in the grid
        self.on_cell_click = on_cell_click # function to call when ...
        self.cells = {} # Set of all cells in the grid
        self.on_cell_click = on_cell_click # function to call when ...

    def setup_grid(self):
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)  # Spacing between cells



        for row in range(self.grid_size):
            for col in range(self.grid_size):
                cell = QPushButton("") # cell button
                cell.setMinimumSize(150, 150)
                cell.clicked.connect(lambda _, r=row, c=col: self.on_cell_click(r, c))
                cell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                cell.setProperty("class", "grid-cell")
                # Ensure the button has no text or icon
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
        """ Reset the grid to its initial state for a new game
        T"""

        for cell in self.cells.values():
            cell.setIcon(QIcon())  # Clear the icon
            cell.setEnabled(True)  # Enable to click on the cell
            cell.setStyleSheet("")  # Reset style to default version
            cell.setProperty("class", "grid-cell")  # Reapply the grid-cell class

    def set_button_state(self, row: int, col: int, is_bomb: bool, revealed: bool = False) -> None:
        """ Changes the image and style of a cell accessing its buttons via its coordinates """
        cell = self.cells[(row, col)]
        
        if is_bomb:
            icon = QIcon("utils/imgs/cells/bomb.png")
            
        else:
            icon = QIcon("utils/imgs/cells/star.png")
           
        cell.setIcon(icon)
        cell.setIconSize(QSize(170, 170))  # Adjust size as needed
        


    def disable_button(self, row:int, col:int) -> None:
        self.cells[(row, col)].setDisabled(True)

    def reveal_cells(self, set_of_mines: set, clicked_cells: set) -> None:
        # Showing all other mines
        non_clicked_cells = set(self.cells.keys()).difference(clicked_cells)
        # Revealing unclicked cells
        for row, col in non_clicked_cells:
            if (row, col) in set_of_mines:
                self.set_button_state(row, col, True, revealed=True)
            else:
                self.set_button_state(row, col, False, revealed=True)

    def reveal_cells(self, set_of_mines: set, clicked_cells: set) -> None:
        # Showing all other mines
        non_clicked_cells = set(self.cells.keys()).difference(clicked_cells)
        # Revealing unclicked cells
        for row, col in non_clicked_cells:
            if (row, col) in set_of_mines:
                self.set_button_state(row, col, True)
            else:
                self.set_button_state(row, col, False)