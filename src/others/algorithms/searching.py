import pandas as df

class MySearching():
    def binary_search_users(self, arr:df.DataFrame, username):
        left, right = 0, len(arr) - 1
    
        while left <= right:
            mid = (left + right) // 2
            mid_username = arr.iloc[mid]['username']  # Get the username at the midpoint
            
            # If the target is found
            if mid_username == username:
                return arr.iloc[mid]['rank']
            
            elif username > mid_username:
                right = mid - 1  # Target is to the left (higher alphabetically)
            else:
                left = mid + 1  # Target is to the right (lower alphabetically)
        
        return None  # If the username is not found