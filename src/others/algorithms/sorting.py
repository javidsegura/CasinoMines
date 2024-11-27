

class MySorting():
      def __init__(self, index, ascending=False):
            """
            Analysis (for merge sort):
                  - Time complexity: O(n log n) / worst and best case
                  - Space complexity: O(1)
            Parametes:
                  - index is the subscripting part of the array (the value to sort by)
            """
            self.index = index
            self.ascending = ascending 

      def evaluate(self, l:list , r:list) -> bool:
            """ Returns True when left element is added to arr first """
            if self.ascending:
                  return l[self.index] >= r[self.index]
            else:
                  return l[self.index] <= r[self.index]

      def mergeSort(self, arr: list[list], left: int, right: int) -> None:
            """ Sorts array in place"""

            if left < right - 1:
                  mid = (left + right) // 2
                  self.mergeSort(arr, left, mid)
                  self.mergeSort(arr, mid, right)
                  self.merge(arr, left, mid, right)

      def merge(self, arr: list[list], left: int, mid: int, right: int) -> None:
            """ right is inclusive of mid, Right is subscriptable in arr"""

            # Create temporary subarrays
            n_l = mid - left
            n_r = right - mid

            left_arr = [0] * n_l
            right_arr = [0] * n_r

            for i in range(n_l):
                  left_arr[i] = arr[left + i]
            for j in range(n_r):
                  right_arr[j] = arr[mid + j]
                        
            i = j = 0
            k = left

            while i < n_l and j < n_r:
                  if self.evaluate(left_arr[i], right_arr[j]):
                        arr[k] = left_arr[i]
                        i += 1
                  else:
                        arr[k] = right_arr[j]
                        j += 1
                  k += 1

            while i < n_l:
                  arr[k] = left_arr[i]
                  k += 1
                  i += 1

            while j < n_r:
                  arr[k] = right_arr[j]
                  k += 1
                  j += 1




# TESTING
if __name__ == "__main__":
      temp = MySorting(1, ascending=True)
      arr = [[6, 1], [7, 2], [8, 3], [4, 4], [3, 5], [2, 6], [-1, 9]]
      temp.mergeSort(arr, 0, len(arr))
      print(arr)
