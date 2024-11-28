class Wallet:
    """ Controls the logic of the wallet of the game"""
    def __init__(self, initial_balance=1000) -> None:
        """
        Description: defines payment logic of the game
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.balance = initial_balance # Money in the account
        self.current_bet = 0 # Current bet
        self.current_multiplier = 1 # Current multiplier
        self.profit = 0 # Current profit
        self.prior_profit = 0 # Prior profit
        self.prior_multiplier = 1 # Prior multiplier

    def place_bet(self, amount) -> None:
        """
        Description: places a bet
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.current_bet = amount
        self.balance -= amount

    def update_multiplier(self, new_multiplier) -> None:
        """
        Description: stores prior multiplier
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.current_multiplier = new_multiplier

    def cash_out(self) -> float:
        """
        Description: cashes out the current bet
        Time Complexity:
            - O(1): All operations run in constant time
        """
        winnings = self.current_bet * self.current_multiplier
        self.balance += winnings
        self.prior_profit = self.calculate_profit()
        self.prior_multiplier = self.current_multiplier
        self.reset_bet()

        return winnings

    def reset_bet(self) -> None:
        """
        Description: resets the wallet account values
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.current_bet = 0
        self.current_multiplier = 1
        self.profit = 0
        self.profit = 0

    def get_balance(self) -> float:
        """
        Description: gets the balance
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.balance

    def get_current_bet(self) -> float:
        """
        Description: gets the current bet
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.current_bet

    def get_current_multiplier(self) -> float:
        """
        Description: gets the current multiplier
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return self.current_multiplier

    def calculate_percentage_bet(self, percentage) -> float:
        """
        Description: calculates the percentage bet
        Time Complexity:
            - O(1): All operations run in constant time
        """
        return abs(self.balance) * (percentage / 100)
    
    def calculate_profit(self) -> float:
        """
        Description: calculates the profit
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.profit = self.current_bet * self.current_multiplier - self.current_bet
        return self.profit
    
    def increase_balance(self, amount) -> float:
        """
        Description: increases the balance
        Time Complexity:
            - O(1): All operations run in constant time
        """
        self.balance += amount
        return self.balance
        
