"""
Controls all the logic related to the bombs
"""

import random

class MinesLogic():
    """ Controls the logic of the mines """

    def __init__(self, grid_size:int=5) -> None:
        """ Initializes the mines logic
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.grid_size = grid_size
        self.mines = set() # Here we will set the coordinates of the mines

    def get_mines_set(self, num_mines:int) -> None:
        """
        Description: creates the set with the mines coordinates
        Time Complexity:
            - Worst case: O(n^2): where n is the number of the mines and the second n is given by a very poor hashing function that collision every time it tries to insert 
            - Average case: O(n): where n is the number of the mines and the second n is given by a very good hashing function that never collides (O(1) insertion on set)
        """
        self.num_mines = num_mines
        self.mines.clear() # Remove all elements in the set
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            self.mines.add((row, col))

    def is_mine(self, row:int, col:int) -> bool: 
        """ Determines if the given cell is a mine or not
        Time Complexity:
            - O(1): average case: All operations run in constant time
            - O(n): worst case: where n is the number of the mines and the second n is given by a very poor hashing function that collision every time it tries to insert 
        """
        return (row, col) in self.mines

    def set_of_mines(self) -> set:
        """ Returns the set of mines
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.mines
    

    