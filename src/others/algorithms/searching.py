

class MySearching():
    def binary_search_leaderboard(self, leaderboard_data: list[tuple], userName: str) -> int:
        """ 
            Analysis (for binary search):
                - Time complexity:
                    - Average & Worst: O(log n)
                    - Best: O(1)
                - Space complexity: O(1)
            Parameters:
                - leaderboard_data: list of lists, where each inner list contains four elements: [rank, username, score, time]
                - userName: string, the username to search for in the leaderboard
            Returns:
                - int: the rank of the user if found, -1 otherwise
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