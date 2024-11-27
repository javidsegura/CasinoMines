import random

# grid 5X5
grid_size = 5
# bombs cant be greater than 24 but that case is handled in base case
max_bombs = grid_size ** 2 

def place_bombs(num_bombs: int) -> set:
    # unique coordinates will be stored here (handles duplicates)
    bomb_placement = set()

    #base case: if bombs are == 25 or greater
    if num_bombs >= max_bombs:
        raise ValueError("You can only choose a maximum of 24 bombs")
    
    #while loop until we reach desired number of bombs
    while len(bomb_placement) < num_bombs:
        row = random.randint(0, grid_size - 1)
        column = random.randint(0, grid_size - 1)

        bomb_coordinates = (row, column)
        
        #stores bomb coordinate in set
        bomb_placement.add(bomb_coordinates)
    
    return bomb_placement

# Remember that LCG was used in simulations, where reproducibility
# was essential. In this case, since our only objective is to randomly 
# position the bombs, the built-in function is enough and even more effective. 
# If in the future, we would like to do something like replicating 
# games for users, then LCG method may be more suitable.