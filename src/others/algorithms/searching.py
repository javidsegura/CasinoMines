

class MySearching():
    def binary_search_leaderboard(self, leaderboard_data: list, userRank: str) -> tuple[str, int, int]:
        """ 
            Analysis (for binary search):
            - Time complexity: O(log n) / worst case; O(1) / best case
            - Space complexity: O(1)
        """

        left, right = 0, len(leaderboard_data) - 1
        
        while left <= right:
            mid = (left + right) // 2
            rank = leaderboard_data[mid][0]  
            
            if rank == userRank:
                username = leaderboard_data[mid][1]
                
                start = 1
                if userRank > 5: 
                    start = userRank - 4
                limit = start + 9
                
                # Ensure limit doesn't exceed total players; IS THIS NECESSARY?
                if len(leaderboard_data) < limit:
                    limit = len(leaderboard_data)
                    
                return (username, start, limit)
            
            elif rank < userRank: # move right
                left = mid + 1
            else: # move left
                right = mid - 1
                
        return (-1, 0, 0)  # User not found