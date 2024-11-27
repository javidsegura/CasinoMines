

class MySearching():
    def binary_search_leaderboard(self, leaderboard_data: list[list], userName: str) -> int:
        """ 
            User username as the search key in the leaderboard (sorted by username). Return its rank or -1 if user not found.

            Analysis (for binary search):
            - Time complexity: O(log n) / worst case; O(1) / best case
            - Space complexity: O(1)
        """


        left, right = 0, len(leaderboard_data) - 1
        
        while left <= right:
            mid = (left + right) // 2
            currentUsername = leaderboard_data[mid][1]  
            
            if currentUsername == userName:
                return leaderboard_data[mid][0]
            
            elif currentUsername < userName: # move right
                left = mid + 1
            else: # move left
                right = mid - 1
                
        return -1
    

"""
Invoked in line 214 of leaderboard_ui.py
"""