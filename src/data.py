import csv

class UserData:
    def __init__(self, file_path="utils/data/userData.csv"):
        self.file_path = file_path
    
    # Initialize the CSV with headers
    def initialize_csv(self):
        with open(self.file_path, 'w', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(["id", "betAmount", "numMines", "balanceBefore", "profit", "balanceAfter", "win"])
    
    # Add user data to the CSV
    def add_user_data(self, game_id, bet, bombs, balanceBefore, profit, balanceAfter, win):
        with open(self.file_path, 'a', newline='') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow([game_id, bet, bombs, balanceBefore, profit, balanceAfter, win])
            # csv_writer.writerow([game_id, CasinoMines.getBetMain(), CasinoMines.getBombsMain(), profit])
    
    # Display all user data
    def print_all_user_data(self):
        with open(self.file_path, 'r') as data_file:
            csv_reader = csv.reader(data_file)
            for row in csv_reader:
                print(row)

# # Usage
# if __name__ == "__main__":
#     user_data = UserData()
    
#     # Initialize the CSV with headers
#     user_data.initialize_csv()

#     # Add a user entry (you could loop this or call it as needed)
#     user_data.add_user_data(user_id=1)
    
#     # Print all user data
#     user_data.print_all_user_data()

