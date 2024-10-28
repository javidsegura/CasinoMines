import csv
import os

class UserData:
    def __init__(self, file_path="utils/data/userData.csv", leaderboardPath="utils/data/leaderboard.csv"):
        self.file_path = file_path
        self.leaderboardPath = leaderboardPath
        self.rowToModify = None
        self.userExists = False
        self.numPlayers = 0

        self.leaderboardList = []
    
    # Initialize the CSV with headers
    def initialize_csv(self):
        with open(self.file_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["id", "betAmount", "numMines", "balanceBefore", "profit", "balanceAfter", "win"])

    def initialize_leader(self):
        if os.path.isfile(self.leaderboardPath):
            with open(self.leaderboardPath, 'r') as data_file:
                csv_reader = csv.reader(data_file)
                self.leaderboardList = list(csv_reader)
                self.numPlayers = len(self.leaderboardList) - 1 # -1 for labels row
            print(f"Leaderboard exists: \n{self.leaderboardList}")

        else:
            with open(self.leaderboardPath, 'w', newline='') as data_file:
                csv_writer = csv.writer(data_file)
                csv_writer.writerow(["rank", "user", "largestBalance"])
    
    def return_leaderboard_list(self):
        return self.leaderboardList    

    def return_numPlayers(self):
        return self.numPlayers

    # Add user data to the CSV
    def add_user_data(self, game_id, bet, bombs, balanceBefore, profit, balanceAfter, win):
        with open(self.file_path, 'a', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow([game_id, bet, bombs, balanceBefore, profit, balanceAfter, win])



    def add_leaderboard_data(self, user, balance):
        print(f"\nLeaderboard data is first: {self.leaderboardList}")

        if self.find_highest_balance(user, balance): #user exists and this balance is its highscore
            self.leaderboardList[self.rowToModify] = [0, user, str(balance)]
            # sort leaderboard again
        elif not self.userExists: #user does not exist yet
            self.numPlayers += 1
            self.leaderboardList.append([0, user, str(balance)])
            # sort leaderboard again

        print(f"\nLeaderboard data is then: {self.leaderboardList}")
        self.leaderboardList = [['rank','user','largestBalance']] + self.mergeSort_leaderboard_data(self.leaderboardList[1::], 0, len(self.leaderboardList) - 1)
        print(f"\nSorted leaderboard data is: {self.leaderboardList}")


        with open(self.leaderboardPath, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            for row in self.leaderboardList:
                csv_writer.writerow(row)
        self.userExists = False
        print(f"Leaderboard data is now: {self.leaderboardList}\n")

    def find_highest_balance(self, user, balance):
        for i, row in enumerate(self.leaderboardList):
            if row[1] == user:
                if float(row[2]) <= balance:
                    self.rowToModify = i
                    return True
                self.userExists = True #this only exectues if the user exists but the current balance is not its highscore
        return False


    def mergeSort_leaderboard_data(self, arr, start, end):
        if start < end:
            mid = (start + end) // 2

            # Recursively split and sort both halves
            self.mergeSort_leaderboard_data(arr, start, mid)
            self.mergeSort_leaderboard_data(arr, mid + 1, end)

            # Merge the sorted halves
            self.merge(arr, start, mid, end)
        return arr
    

    def merge(self, arr, start, mid, end):
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
    
    # def mergeSort(self, arr, start, end):
        




    # Display all user data
    def print_all_user_data(self):
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for row in csv_reader:
                print(row)



