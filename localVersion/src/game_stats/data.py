""" Controls the data of the game """

import csv
import os
import math

class UserData():
    def __init__(self, file_path:str="localVersion/utils/data/userData.csv", leaderboardPath:str="localVersion/utils/data/leaderboard.csv") -> None:
        self.file_path = file_path
        self.leaderboardPath = leaderboardPath
        self.rowToModify = None
        self.userExists = False
        self.numPlayers = 0
        self.leaderboardList = [] # arr of records for leaderboard
        self.initialize_game_stats()
        self.initialize_leaderboard()
    
    # Initialize the CSV files
    def initialize_game_stats(self) -> None:
        """ Create game stats csv"""
        with open(self.file_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["id", "betAmount", "numMines", "balanceBefore", "profit", "balanceAfter", "win"])

    def initialize_leaderboard(self) -> None:
        if not os.path.isfile(self.leaderboardPath):
            with open(self.leaderboardPath, 'w', newline='') as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(["rank", "user", "largestBalance"])
                
        with open(self.leaderboardPath, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            self.leaderboardList = list(csv_reader)
            self.numPlayers = len(self.leaderboardList) - 1 # -1 for labels row
        #print(f"Leaderboard exists: \n{self.leaderboardList}")

    # Adding data to the CSV files
    def add_user_data(self, game_id:int, bet:float, bombs:int, balanceBefore:float, profit:float, balanceAfter:float, win:str) -> None:
        """ Add user data to the game stats csv"""
        with open(self.file_path, 'a', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow([game_id, math.floor(bet * 100) / 100, bombs, math.floor(balanceBefore * 100) / 100, math.floor(profit * 100) / 100, math.floor(balanceAfter * 100) / 100, win])

    def add_leaderboard_data(self, user:str, balance:float) -> None:
        """ Add user data to the leaderboard csv"""
        #print(f"\nLeaderboard data is first: {self.leaderboardList}")

        if self.find_highest_balance(user, balance): #user exists and this balance is its highscore
            self.leaderboardList[self.rowToModify] = [0, str(user), str(math.floor(balance * 100) / 100)]
            # sort leaderboard again
        elif not self.userExists: #user does not exist yet
            self.numPlayers += 1
            self.leaderboardList.append([0, str(user), str(math.floor(balance * 100) / 100)])
        
        #print(f"\nLeaderboard data is then: {self.leaderboardList}")
        self.leaderboardList = [['rank','user','largestBalance']] + self.mergeSort_leaderboard_data(self.leaderboardList[1::], 0, len(self.leaderboardList) - 1)
        #print(f"\nSorted leaderboard data is: {self.leaderboardList}")

        # Rewriting the leaderboard csv with ordered data
        with open(self.leaderboardPath, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            for row in self.leaderboardList:
                csv_writer.writerow(row)
        self.userExists = False

    # Manipulating the CSVs
    def find_highest_balance(self, user:str, balance:float) -> bool:
        for i, row in enumerate(self.leaderboardList):
            if row[1] == user:
                if float(row[2]) <= balance:
                    self.rowToModify = i
                    return True
                self.userExists = True #this only exectues if the user exists but the current balance is not its highscore
        return False

    def mergeSort_leaderboard_data(self, arr:list, start:int, end:int) -> list:
        """ Sorting algorithm. 
        O(n log n) time complexity 
        O(n) space complexity: ERROR!!!!!!!
        """
        if start < end:
            mid = (start + end) // 2

            # Recursively split and sort both halves
            self.mergeSort_leaderboard_data(arr, start, mid)
            self.mergeSort_leaderboard_data(arr, mid + 1, end)

            # Merge the sorted halves
            self.merge(arr, start, mid, end)
        return arr
    
    def merge(self, arr:list, start:int, mid:int, end:int) -> None:
        left = arr[start:mid + 1]
        right = arr[mid + 1:end + 1]
        i = j = 0
        k = start

        # Merge the two halves
        while i < len(left) and j < len(right):
            if float(left[i][2]) >= float(right[j][2]):  # Compare based on third element (balance)
                arr[k] = [k + 1] + left[i][1::]
                i += 1
            else:
                arr[k] = [k + 1] + right[j][1::] #assinging rank
                j += 1
            k += 1

        # Copy any remaining elements from the left half
        while i < len(left):
            arr[k] = [k + 1] + left[i][1::]
            i += 1
            k += 1

        # Copy any remaining elements from the right half
        while j < len(right):
            arr[k] = [k + 1] + right[j][1::]
            j += 1
            k += 1    

    # Display all user data
    def print_all_user_data(self) -> None:
        """ is this called at any time? """
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for row in csv_reader:
                print(row)
    
    def return_leaderboard_list(self) -> list:
        return self.leaderboardList    

    def return_numPlayers(self) -> int:
        return self.numPlayers