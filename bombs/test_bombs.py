from bomb_placement import place_bombs 

def test_place_bombs():
    # user should choose number of bombs
    num_bombs = 5
    
    # call function to place bombs
    bomb_positions = place_bombs(num_bombs)
    
    print("Bomb positions:", bomb_positions)

# test
if __name__ == "__main__":
    test_place_bombs()