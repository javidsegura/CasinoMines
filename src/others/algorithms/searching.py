

class MySearching():
    def binary_search_leaderboard(self, leaderboard_data: list, username: str) -> tuple[int, int, int]:
        left, right = 0, len(leaderboard_data) - 1
        
        while left <= right:
            mid = (left + right) // 2
            current_user = leaderboard_data[mid][1]  
            
            if current_user == username:
                userRank = leaderboard_data[mid][0]  
                
                start = 1
                if userRank > 5:
                    start = userRank - 4
                limit = start + 9
                
                # Ensure limit doesn't exceed total players
                if len(leaderboard_data) < limit:
                    limit = len(leaderboard_data)
                    
                return (userRank, start, limit)
            
            elif current_user < username:
                left = mid + 1
            else:
                right = mid - 1
                
        return (-1, 0, 0)  # User not found