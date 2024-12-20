""" Controls the data of the game """

from others.algorithms.sorting import MySorting

import csv
import os
from datetime import date
import pandas as pd

class UserData():
    def __init__(self, game_stats_path:str="utils/data/game_stats.csv", leaderboardPath:str="utils/data/leaderboard.csv") -> None:
        """ Initilaize game data objects
        Time Complexity:
          - O(n): where n is the number of rows in the leaderboard
        """
        self.game_stats_path = game_stats_path
        self.leaderboardPath = leaderboardPath
        self.leaderboardList = []
        self.game_stats_pd = self.initialize_game_stats() # O(1)
        self.leaderboard_pd = self.initialize_leaderboard() # O(n)

    
    # 0) GAME STATS CSV
    def initialize_game_stats(self) -> pd.DataFrame:
        """ Create game stats csv
        Time Complexity:
            - O(1): All operations run in constant time
        """
        with open(self.game_stats_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["gameId", "win","betAmount", "numMines", "balanceBefore", "balanceAfter", "profit"])
        return pd.read_csv(self.game_stats_path)
    
    def add_user_data(self, win:bool, game_id:int, bet:float, mines:int,
                     balanceBefore:float, balanceAfter:float, profit:float) -> None:
        """ Add user data to GAME STATS csv. Invoked at the end of each game
        Time Complexity:
            - O(n): where n is the number of rows in the game_stats_pd
        """

        # Add game stats to game_stats_pd
        new_row = pd.DataFrame([[game_id, win, bet, mines,
                                 balanceBefore, balanceAfter, profit]], 
                               columns=self.game_stats_pd.columns)
        self.game_stats_pd = pd.concat([self.game_stats_pd, new_row], ignore_index=True) # O(n)

        self.write_game_stats_pd() # O(n)

    # 1) LEADERBOARD CSV
    def initialize_leaderboard(self) -> pd.DataFrame:
        """ Initializes leaderboard data
        Time Complexity:
            - O(n): where n is the number of rows in the leaderboard
        """
        if not os.path.isfile(self.leaderboardPath):
            with open(self.leaderboardPath, 'w', newline='') as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(["rank", "username", "largestBalance", "date"]) 
        return pd.read_csv(self.leaderboardPath)
    
    def add_leaderboard_data(self, user:str, balance:float) -> None:
        """ 
        Invoked at the end of each game.
        Time Complexity:
            - O(n * log(n)): where n is the number of rows in the leaderboard
        """
        # Find if user has already played:
        all_users_names = self.leaderboard_pd["username"].tolist() # No support for .toset() method
        if user in all_users_names: # O(n)
            aggregate_old_user, user_rank = self.find_highest_balance(user, balance)
            if aggregate_old_user: 
                self.leaderboard_pd.loc[user_rank] = [0, 
                                                   user, 
                                                   round(balance, 2), 
                                                   date.today()]  # arbitrary rank of 0
        else: 
            new_row = pd.DataFrame([[0,
                                      user, 
                                      round(balance, 2), 
                                      date.today()]], 
                                 columns=self.leaderboard_pd.columns)
            self.leaderboard_pd = pd.concat([self.leaderboard_pd, new_row], ignore_index=True)

        # Sort leaderboard CSV
        leaderboard_list = self.leaderboard_pd.values.tolist()
        MySorting(self.leaderboard_pd.columns.get_loc("largestBalance"), ascending=True).mergeSort(leaderboard_list, 
                                                                                                 0, 
                                                                                                 len(leaderboard_list)) # O(n * log n)
        # Write to database
        self.sortedLeaderboardList = leaderboard_list
        self.write_leaderboard_pd(self.sortedLeaderboardList) # O(n)

    # 2) Auxiliary functions
    def find_highest_balance(self, user:str, balance:float) -> bool:
        """ Returns True if current balance is the highest balance for the user and its prior rank.
        Time Complexity:
            - O(n): where n is the number of rows in the leaderboard
        """
       
        # Find the index of the user in the leaderboard
        user_index = self.leaderboard_pd[self.leaderboard_pd["username"] == user].index[0]
        if self.leaderboard_pd.loc[user_index, "largestBalance"] >= balance:
            return False, None
        else:
            return True, user_index

    def return_leaderboard_list(self) -> list:
        """ Transforms pandas DF to list
        Time Complexity:
            - O(n): where n is the number of rows in the leaderboard
        """
        return self.leaderboard_pd.values.tolist()    

    def return_numPlayers(self) -> int:
        """ Defines number of players on leaderboard
        Time Complexity:
            - O(1): All operations run in constant time
        """
        if self.leaderboard_pd is not None:
            return self.leaderboard_pd.shape[0] - 1
        else:
            return 0
    
    def empty_csv(self, filepath: str) -> None:
        """ Empty the contents of a CSV file
        Time Complexity:
            - O(1): All operations run in constant time
        """
        with open(filepath, 'w', newline=''):
            pass
    
    def write_leaderboard_pd(self) -> None:
        """ Writes leaderboard data to leaderboard.csv
        Time Complexity:
            - O(n): where n is the number of rows in the leaderboard
        """
        self.leaderboard_pd["rank"] = range(1, len(self.leaderboard_pd) + 1) # Adding the rank col before write
        self.leaderboard_pd.to_csv(self.leaderboardPath, index=False)
    
    def write_game_stats_pd(self) -> None:
        """ Writes game data to game_stats.csv
        Time Complexity:
            - O(n): where n is the number of rows in the game_stats_pd
        """
        self.game_stats_pd.to_csv(self.game_stats_path, index=False)
    
    def write_leaderboard_pd(self, leaderboard_pd: pd.DataFrame) -> None:
        """ Writes leaderboard data to leaderboard.csv
        Time Complexity:
            - O(n): where n is the number of rows in the leaderboard
        """
        self.leaderboard_pd = pd.DataFrame(leaderboard_pd, 
                                            columns=self.leaderboard_pd.columns)
        self.leaderboard_pd["rank"] = range(1, len(self.leaderboard_pd) + 1)
        self.leaderboard_pd.to_csv(self.leaderboardPath, index=False)
    


if __name__ == "__main__":
      # Testing
      temp = UserData()
      temp.add_leaderboard_data("caye", -10000)
      print(f"Leaderboard: {temp.return_leaderboard_list()}")
      