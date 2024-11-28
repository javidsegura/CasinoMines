"""Includes all the math behind the multiplier function."""

from math import factorial    
import pandas as pd

class MultiplierFunc():
    """
    Get the multiplier function for the given game set-up. 
    The multiplier function is a function of the frequency function and the house advantage.
    
    """
    def __init__(self, n:int, r:int, b:int = 1, M:int = .03) -> None:
        """
        Description: initializes the MultiplierFunc class
        Time Complexity:
            - O(1): All operations run in constant time
        Parameters:
            - n = number of cells
            - r = number of bombs in the cell
            - b = bet amount (in monetary units)
            - M = house advantage (in percentage)

        Returns:
            None 
        
        """
        
        self.n = n
        self.r = r
        self.b = b
        self.M = M

    def probability_distribution(self, x:int) -> int:
        """
        Definition:
            Computes the probability of clearing x space in the given setup of the game (refer to 1.1 in the presence of doubt)
        Time Complexity:
            - O(1): All operations run in constant time
        Parameters:
            - x = number of spaces to clean
        Returns:
            probability frequency"""
        
        numerator = factorial(self.n-self.r) * factorial(self.n-x)
        denominator = factorial(self.n) * factorial(self.n-self.r-x)

        return numerator / denominator # Frequency

    def frequency_table(self) -> pd.DataFrame:
        """
        Definition:
            Computes all the possible cell clean-ups scenarios.
        Time Complexity:
            - O(n): where n is the number of cells. Please note that this is asymptotic growth, 
            ignoring the fact that self.n is a constant value.
        Parameters:
            None
        Returns:
            Pandas dataframe with the results for each possible x."""
        
        frequencies_table = dict()
        x = 0
        while self.n-self.r-x >= 0: # As long as you can make non-negative moves
            frequencies_table[x] = self.probability_distribution(x)
            x += 1

        self.results_table = pd.DataFrame(list(frequencies_table.items()), columns=["SpaceUncovered", "WinFrequency"])
        self.results_table["Multiplier"] = 1/self.results_table["WinFrequency"] * (1-self.M) # Multiplier function
        
        return self.results_table.round(2) # Round up all cols' values to 2 decimals
    
    def get_next_multiplier(self,index) -> float:
        """
        Description:
            Get the next multiplier for the given index.
        Time Complexity:
            - O(n): where n is the number of cells. Please note that this is asymptotic growth, 
            ignoring the fact that self.n is a constant value.
        """
        frequency_table = self.frequency_table()[1:]

        return frequency_table.iloc[index]["Multiplier"]
    
  


