""" Controls the data of the game """

from others.algorithms.sorting import MySorting

import csv
import os
import math
from datetime import date
import pandas as pd

class UserData():
    def __init__(self, game_stats_path:str="utils/data/game_stats.csv", leaderboardPath:str="utils/data/leaderboard.csv") -> None:
        """ Initilaize game data objects
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
        """
        self.game_stats_path = game_stats_path
        self.leaderboardPath = leaderboardPath
        self.leaderboardList = []
        self.game_stats_pd = self.initialize_game_stats()
        self.leaderboard_pd = self.initialize_leaderboard()

    
    # 0) GAME STATS CSV
    def initialize_game_stats(self) -> pd.DataFrame:
        """ Create game stats csv
        Time Complexity:
            Worst Case: O(1)
            Avg Case: O(1)
        """
        with open(self.game_stats_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["gameId", "win","betAmount", "numMines", "balanceBefore", "balanceAfter", "profit"])
        return pd.read_csv(self.game_stats_path)
    
    def add_user_data(self, win:bool, game_id:int, bet:float, mines:int,
                     balanceBefore:float, balanceAfter:float, profit:float) -> None:
        """ Add user data to GAME STATS csv. Invoked at the end of each game
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
        """

        # Add game stats to game_stats_pd
        new_row = pd.DataFrame([[game_id, win, bet, mines,
                                 balanceBefore, balanceAfter, profit]], 
                               columns=self.game_stats_pd.columns)
        self.game_stats_pd = pd.concat([self.game_stats_pd, new_row], ignore_index=True)

        self.write_game_stats_pd()

    # 1) LEADERBOARD CSV
    def initialize_leaderboard(self) -> pd.DataFrame:
        """ Initializes leaderboard data
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
        """
        if not os.path.isfile(self.leaderboardPath):
            with open(self.leaderboardPath, 'w', newline='') as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(["rank", "username", "largestBalance", "date"]) 
        return pd.read_csv(self.leaderboardPath)
    
    def add_leaderboard_data(self, user:str, balance:float) -> None:
        """ Add user data to LEADERBOARD csv and sorted based on balance. Invoked at the end of each game.
        Time Complexity:
            Worst Case: O(n log n)
            Avg Case: O(n log n)
        """
        # Find if user has already played:
        all_users_names = self.leaderboard_pd["username"].tolist()
        if user in all_users_names: 
            aggregate_old_user, user_rank = self.find_highest_balance(user, balance)
            if aggregate_old_user: 
                self.leaderboard_pd.loc[user_rank] = [0, 
                                                   user, 
                                                   round(balance, 2), 
                                                   date.today()]  # arbitrary rank for 0
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
                                                                                                 len(leaderboard_list)) 
        self.sortedLeaderboardList = leaderboard_list
        self.leaderboard_pd = pd.DataFrame(leaderboard_list, 
                                            columns=self.leaderboard_pd.columns)
        
        self.write_leaderboard_pd()

    # 2) Auxiliary functions
    def find_highest_balance(self, user:str, balance:float) -> bool:
        """ Returns True if current balance is the highest balance for the user and its prior rank.
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
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
            Worst Case: O(n)
            Avg Case: O(n)
        """
        return self.leaderboard_pd.values.tolist()    

    def return_numPlayers(self) -> int:
        """ Defines number of players on leaderboard
        Time Complexity:
            Worst Case: O(1)
            Avg Case: O(1)
        """
        if self.leaderboard_pd is not None:
            return self.leaderboard_pd.shape[0] - 1
        else:
            return 0
    
    def empty_csv(self, filepath: str) -> None:
        """ Empty the contents of a CSV file
        Time Complexity:
            Worst Case: O(1)
            Avg Case: O(1)
        """
        with open(filepath, 'w', newline=''):
            pass
    
    def write_leaderboard_pd(self) -> None:
        """ Writes leaderboard data to leaderboard.csv
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
        """
        self.leaderboard_pd["rank"] = range(1, len(self.leaderboard_pd) + 1)
        self.leaderboard_pd.to_csv(self.leaderboardPath, index=False)
    
    def write_game_stats_pd(self) -> None:
        """ Writes game data to game_stats.csv
        Time Complexity:
            Worst Case: O(n)
            Avg Case: O(n)
        """
        self.game_stats_pd.to_csv(self.game_stats_path, index=False)
    


if __name__ == "__main__":
      temp = UserData()
      temp.add_leaderboard_data("javi", -10000)
      print(f"Leaderboard: {temp.return_leaderboard_list()}")