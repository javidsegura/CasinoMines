

class MergeSort():
      def __init__(self, index, reverse=False):
            """
            index is the subscripting part of the array
            """
            self.index = index
            self.reverse = reverse 

      def mergeSort(self, arr: list[list], left: int, right: int):
            """right is exclusive for right arr
               mid is exclusive for left arr
               => right - left represents the length of the subset of the arr"""
            if left < right - 1:
                  mid = (left + right) // 2
                  self.mergeSort(arr, left, mid)
                  self.mergeSort(arr, mid, right)
                  self.merge(arr, left, mid, right)



      def merge(self, arr: list[list], left: int, mid: int, right: int):
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
                  if left_arr[i][self.index] <= right_arr[j][self.index]:
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






if __name__ == "__main__":
      temp = MergeSort(0)
      arr = [[6, 1], [7, 2], [8, 3], [4, 4], [3, 5], [2, 6]]
      temp.mergeSort(arr, 0, len(arr))
      print(arr)
