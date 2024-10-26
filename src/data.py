import csv

class UserData:
    def __init__(self, file_path="utils/data/userData.csv", leaderboardPath="utils/data/leaderboard.csv"):
        self.file_path = file_path
        self.leaderboardPath = leaderboardPath
        self.rowToModify = None
        self.userExists = False
    
    # Initialize the CSV with headers
    def initialize_csv(self):
        with open(self.file_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["id", "betAmount", "numMines", "balanceBefore", "profit", "balanceAfter", "win"])

    def initialize_leader(self):
        with open(self.leaderboardPath, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["user", "largestBalance"])
    
    # Add user data to the CSV
    def add_user_data(self, game_id, bet, bombs, balanceBefore, profit, balanceAfter, win):
        with open(self.file_path, 'a', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow([game_id, bet, bombs, balanceBefore, profit, balanceAfter, win])



    def add_leaderboard_data(self, user, balance):
        print(f"\nSelf.data is first: {self.data}")
        with open(self.leaderboardPath, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            self.data = []
            self.data = list(csv_reader) #each time something is added to userData, self.data updates

        if self.find_highest_balance(user, balance): #user exists and this balance is its highscore
            self.data[self.rowToModify] = [user, balance]
        elif not self.userExists: #user does not exist yet
            self.data.append([user, balance])

        with open(self.leaderboardPath, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(self.data)
        self.userExists = False
        print(f"Self.data is now: {self.data}\n")

    def find_highest_balance(self, user, balance):
        for i, row in enumerate(self.data):
            if row[0] == user:
                if row[1] <= balance:
                    self.rowToModify = i
                    return True
                self.userExists = True #this only exectues if the user exists but the current balance is not its highscore
        return False


    # Display all user data
    def print_all_user_data(self):
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for row in csv_reader:
                print(row)



