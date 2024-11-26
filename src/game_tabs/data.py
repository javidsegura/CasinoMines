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
        self.game_stats_pd = self.initialize_game_stats()
        self.leaderboard_pd = self.initialize_leaderboard()
        self.leaderboard_dict = None
        self.userSortLeaderboard = None

    def updateVars(self, leaderboard_dict:dict, leaderboard_df:pd.DataFrame, userSortLeaderboard:pd.DataFrame) -> None:
        self.leaderboard_dict = leaderboard_dict
        self.leaderboard_pd = leaderboard_df
        self.userSortLeaderboard = userSortLeaderboard
        # Only used once upon initilization, when main updates these values based on the possibly new username

    def getChangedVars(self):
        return self.leaderboard_pd, self.leaderboard_dict, self.userSortLeaderboard 
        #These are updated whenever leaderboard changes; leaderboard tab needs this

    
    # 0) GAME STATS CSV
    def initialize_game_stats(self) -> pd.DataFrame:
        """ Create game stats csv"""
        with open(self.game_stats_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["gameId", "win","betAmount", "numMines", "balanceBefore", "balanceAfter", "profit"])
        return pd.read_csv(self.game_stats_path)
    
    def add_user_data(self, win:bool, game_id:int, bet:float, mines:int,
                     balanceBefore:float, balanceAfter:float, profit:float) -> None:
        """ Add user data to GAME STATS csv. Invoked at the end of each game"""

        # Add game stats to game_stats_pd
        new_row = {'gameId': game_id, 'win': win, 'betAmount': bet, 'numMines': mines, 'balanceBefore': balanceBefore, 'balanceAfter': balanceAfter, 'profit': profit}
        self.game_stats_pd = pd.concat([self.game_stats_pd, pd.DataFrame([new_row])], ignore_index=True)

        self.write_game_stats_pd()

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

        # Find if user has already played in O(1):

        aggregate_old_user, user_index = self.find_highest_balance(user, balance)
        if aggregate_old_user: 
            self.leaderboard_pd.loc[user_index] = [0, 
                                                user, 
                                                round(balance, 2), 
                                                date.today()]  # arbitrary rank for 0


        # Sort leaderboard CSV
        # CHANGE SORTING TO PD
        leaderboard_list = self.leaderboard_pd.values.tolist()
        MySorting(self.leaderboard_pd.columns.get_loc("largestBalance"), ascending=True).mergeSort(
            leaderboard_list, 0, len(leaderboard_list)
        ) 
        self.leaderboard_pd = pd.DataFrame(leaderboard_list, 
                                            columns=self.leaderboard_pd.columns)
        self.write_leaderboard_pd()

    # 2) Auxiliary functions
    def find_highest_balance(self, user:str, balance:float) -> bool:
        """ Returns True if current balance is the highest balance for the user and its prior rank.
        """
        # Find the index of the user in the leaderboard in constant time complexity
        user_index = self.leaderboard_dict[user] - 1 #Rank minus 1 is always index
        if self.leaderboard_pd.loc[user_index, "largestBalance"] >= balance:
            return False, None
        else:
            return True, user_index

    def return_leaderboard_list(self) -> pd.DataFrame:
        return self.leaderboard_pd 
        # Only used once in the initlization of main to get leader board data

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
        # New Ranks
        self.leaderboard_pd["rank"] = range(1, len(self.leaderboard_pd) + 1)
        self.leaderboard_dict = dict(zip(self.leaderboard_pd['username'], self.leaderboard_pd['rank']))

        # Sort df in respect to usernames with the new ranks
        self.userSortLeaderboard = list(zip(self.leaderboard_pd['rank'], self.leaderboard_pd['username']))
        MySorting(1, ascending=True).mergeSort(
            self.userSortLeaderboard, 0, len(self.leaderboard_pd)
        )
        self.userSortLeaderboard = pd.DataFrame(self.userSortLeaderboard, columns=['rank', 'username'])
        self.leaderboard_pd.to_csv(self.leaderboardPath, index=False)
    
    def write_game_stats_pd(self) -> None:
        self.game_stats_pd.to_csv(self.game_stats_path, index=False)
    


if __name__ == "__main__":
      temp = UserData()
      temp.add_leaderboard_data("javi", -10000)
      print(f"Leaderboard: {temp.return_leaderboard_list()}")
