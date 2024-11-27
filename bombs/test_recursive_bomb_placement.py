# test_bomb_placement.py
from bomb_placement_recursively import place_bombs  # Adjust according to your file name

def test_place_bombs():
    try:
        # Test with a valid number of bombs
        num_bombs = 5
        bomb_grid = place_bombs(num_bombs)
        print(f"Grid for {num_bombs} bombs:")
        for row in bomb_grid:
            print(row)  # Print each row of the grid


    except ValueError as e:
        print(e)

if __name__ == "__main__":
    test_place_bombs()






