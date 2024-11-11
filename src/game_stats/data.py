""" Controls the data of the game """

from others.algorithms.sorting import MySorting

import csv
import os
import math
from datetime import date
import pandas as pd

class UserData():
    def __init__(self, game_stats_path:str="utils/data/game_stats.csv", leaderboardPath:str="utils/data/leaderboard.csv") -> None:
        self.game_stats_path = game_stats_path
        self.leaderboardPath = leaderboardPath
        self.leaderboardList = [] # arr of records for leaderboard => [user, largestBalance]
        self.game_stats_pd = self.initialize_game_stats()
        self.leaderboard_pd = self.initialize_leaderboard()

    
    # 0) GAME STATS CSV
    def initialize_game_stats(self) -> None:
        """ Create game stats csv"""
        with open(self.game_stats_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["id", "betAmount", "numMines", "balanceBefore", "profit", "balanceAfter", "win"])
        return pd.read_csv(self.game_stats_path)
    
    def add_user_data(self, game_id:int, bet:float, bombs:int, balanceBefore:float, profit:float, balanceAfter:float, win:str) -> None:
        """ Add user data to GAME STATS csv. Invoked at the end of each game"""

        with open(self.game_stats_path, 'a', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow([game_id, math.floor(bet * 100) / 100,
                                  bombs, math.floor(balanceBefore * 100) / 100,
                                  math.floor(profit * 100) / 100, math.floor(balanceAfter * 100) / 100, win])

    # 1) LEADERBOARD CSV
    def initialize_leaderboard(self) -> pd.DataFrame:
        """ Start leaderboard pandas dataframe"""
        if not os.path.isfile(self.leaderboardPath):
            with open(self.leaderboardPath, 'w', newline='') as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(["rank", "username", "largestBalance", "date"]) 
        return pd.read_csv(self.leaderboardPath)
    
    def add_leaderboard_data(self, user:str, balance:float) -> None:
        """ Add user data to LEADERBOARD csv and sorted based on balance
        
        Invoked at the end of each game.
        """

        #print(f"Gonna add leaderboard data. User: {user}, Balance: {balance}")
        # Find if user has already played:
        all_users_names = self.leaderboard_pd["username"].tolist()
        if user in all_users_names: 
            aggregate_old_user, user_rank = self.find_highest_balance(user, balance)
            if aggregate_old_user: 
                self.leaderboard_pd.loc[user_rank] = [0, 
                                                   user, 
                                                   round(balance, 2), 
                                                   date.today()]  # arbitrary rank for 0
            #else:
                #print("Not a record")
        else: 
            new_row = pd.DataFrame([[0,
                                      user, 
                                      round(balance, 2), 
                                      date.today()]], 
                                 columns=self.leaderboard_pd.columns)
            self.leaderboard_pd = pd.concat([self.leaderboard_pd, new_row], ignore_index=True)

        # Sort leaderboard CSV
        leaderboard_list = self.leaderboard_pd.values.tolist()
        #print(f"Leaderboard list: {leaderboard_list}")
        MySorting(self.leaderboard_pd.columns.get_loc("largestBalance"), ascending=True).mergeSort(leaderboard_list, 
                                                                                                 0, 
                                                                                                 len(leaderboard_list)) 
        self.leaderboard_pd = pd.DataFrame(leaderboard_list, 
                                            columns=self.leaderboard_pd.columns)
        #print(f"Sorted leaderboard: {self.leaderboard_pd}")
        self.write_leaderboard_pd()
        #print("\n--------------------------------\n")

    # 2) Auxiliary functions
    def find_highest_balance(self, user:str, balance:float) -> bool:
        """ Returns True if current balance is the highest balance for the user and its prior rank.
        """
        """ HASH TABLEEEEEE"""

        # Find the index of the user in the leaderboard
        user_index = self.leaderboard_pd[self.leaderboard_pd["username"] == user].index[0]
        if self.leaderboard_pd.loc[user_index, "largestBalance"] >= balance:
            return False, None
        else:
            return True, user_index

    def return_leaderboard_list(self) -> list:
        return self.leaderboard_pd.values.tolist()    

    def return_numPlayers(self) -> int:
        if self.leaderboard_pd is not None:
            return self.leaderboard_pd.shape[0] - 1
        else:
            return 0
    
    def empty_csv(self, filepath: str) -> None:
        """Empty the contents of a CSV file while preserving it"""
        with open(filepath, 'w', newline=''):
            pass
    
    def write_leaderboard_pd(self) -> None:
        self.leaderboard_pd["rank"] = range(1, len(self.leaderboard_pd) + 1)
        self.leaderboard_pd.to_csv(self.leaderboardPath, index=False)
    
    def write_game_stats_pd(self) -> None:
        self.game_stats_pd.to_csv(self.game_stats_path, index=False)
    


if __name__ == "__main__":
      temp = UserData()
      temp.add_leaderboard_data("javi", -10000)
      print(f"Leaderboard: {temp.return_leaderboard_list()}")