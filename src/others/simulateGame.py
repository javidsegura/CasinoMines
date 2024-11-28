from multiplier import MultiplierFunc
import random
import pandas as pd
from datetime import datetime
class SimulateGame:
      def __init__(self, numberOfGames:int) -> None:
            """
            Description: initializes the SimulateGame class
            Time Complexity:
                - O(1): All operations run in constant time
            """
            self.numberOfGames = numberOfGames # Number of games per set up
            self.results_data = []  # Add this to store results
      
      #O(m * n) where m is the number of games and n is the number of bombs
      def start_simulation(self):
            """
            Description: starts the simulation
            Time Complexity:
                - O(m * n): where m is the number of games and n is the number of bombs. Please note that this is asymptotic growth, 
                ignoring the fact that the outermost loop has a constant iteration bound of [1,25).
            Notes:      
                - You can tweak the following:
                    - Number of mines
                    - Bet amount (will be kept fixed, we are interested in the percentage)
                    - House advantage
            """
            avg_profit = 0 # Profit on the user 
            for n_of_mines in range(1,25):
                  round_profit = 0
                  games_won = 0
                  games_lost = 0
                  total_rounds_played = 0
                  
                  print(f"Starting game with {n_of_mines} mines")
                  for game_num in range(self.numberOfGames):
                        print(f"\t=> Simulating {game_num+1}th game")
                        game_profit, rounds_played, won = self.simulate_game(n_of_mines)
                        round_profit += game_profit
                        total_rounds_played += rounds_played
                        games_won += 1 if won else 0
                        games_lost += 0 if won else 1
                        print(f"\t\t=> Game profit: {game_profit}")
                   
                  # Store results for this mine configuration
                  self.results_data.append({
                        'mines': n_of_mines,
                        'total_profit': round_profit,
                        'avg_profit': round_profit / self.numberOfGames,
                        'games_won': games_won,
                        'games_lost': games_lost,
                        'win_rate': games_won / self.numberOfGames,
                        'avg_rounds_played': total_rounds_played / self.numberOfGames
                  })
                  
                  avg_profit += round_profit / self.numberOfGames
                  print(f"\nFINISHED PLAYING WITH {n_of_mines} MINES => ROUND PROFIT: {round_profit}\n")
                  print("----------------------------------\n")

            # Create DataFrame and save to CSV
            df = pd.DataFrame(self.results_data) 
            df.to_csv(f'./utils/data/simulations/game_simulation_results{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False)
            return avg_profit

      def simulate_game(self, n_of_mines:int):
            """
            Simulates a single game with the given number of mines.
            Time Complexity:
                - O(n): because of the frequency table's function invocation
            """
            profit = 0

            # 0. Setting up the multiplier function
            multiplierFunc = MultiplierFunc(25, n_of_mines, M=0.1)
            multiplier_table = multiplierFunc.frequency_table() # O(n)

            # 1. Setting up the cells and mines
            cells = set() # coordinates of all cells
            mines = set() # coordinates of all bombs
            for row in range(5):
                  for col in range(5):
                        cells.add((row, col)) # a single coordinate
            
            # 2. Randomly setting bombs
            while len(mines) < n_of_mines:
                  row = random.randint(0, 4)
                  col = random.randint(0, 4)
                  mines.add((row, col))

            #3. Select when player will cash out
            cash_out_round = random.randint(1, 25-n_of_mines)

            print(f"\t\t=> Cash out at round {cash_out_round}")

            # 4. Simulate player choice
            clicked_bomb = False
            number_of_rounds = 0
            while not clicked_bomb and number_of_rounds < cash_out_round :
                  number_of_rounds += 1
                  row = random.randint(0, 4)
                  col = random.randint(0, 4)
                  if (row, col) in mines:
                        clicked_bomb = True
                        print(f"\t\t!> Bomb clicked at round {number_of_rounds}")
                        profit -= 1
                        break
                  else:
                        profit += multiplierFunc.get_next_multiplier(number_of_rounds-1)

            if not clicked_bomb:
                  print(f"\t\t$> Cashed out with {profit}")
                  won = True
            else:
                  won = False

            return profit, number_of_rounds, won

if __name__ == "__main__":   
      simulateGame = SimulateGame(1000)
      avg_simulation = 0

      n_of_simulations = 3

      for i in range(n_of_simulations):
            temp = simulateGame.start_simulation()
            avg_simulation += temp

      print(avg_simulation/n_of_simulations)                  




            
      
      

