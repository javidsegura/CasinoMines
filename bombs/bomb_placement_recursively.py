import random

# grid 5X5
grid_size = 5
# bombs cant be greater than 24 and it is handled in the base case condition
max_bombs = grid_size ** 2  

# function that returns the bombs' coordinates
def place_bombs(num_bombs: int) -> set:
    # base case
    if num_bombs < 1 or num_bombs >= max_bombs:
        raise ValueError("The number of bombs must be between 1 and 24.")
    
    # unique coordinates will be stored here (handles duplicates)
    bomb_placement = set()
    
    # 2D list to create grid where each "sublist" is a row in the grid
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # function that runs until all bombs are placed
    def backtrack(placed_bombs):
        # base case, when all desired amount of bombs are placed function doesn run again
        if placed_bombs == num_bombs:
            return True
        
        # randomly creates coordinates on grid 
        row = random.randint(0, grid_size - 1)
        column = random.randint(0, grid_size - 1)

        # condition checks if there are bombs on a space 
        if grid[row][column] == 0: 
            #places bomb if there are no bombs in empty space 
            grid[row][column] = 1  
            # bomb_placemnt keeps track of used coordinates
            bomb_placement.add((row, column))  

            # function calls itseld and adds 1 placed_bombs that keeps track it 
            if backtrack(placed_bombs + 1):
                return True
            

        # (handles duplicates) if bomb wasn't able to be placed, it tries again
        return backtrack(placed_bombs)

    # starts function with 0 bombs since no bombs are placed before running function
    backtrack(0)

    return grid


