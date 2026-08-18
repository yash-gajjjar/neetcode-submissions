class Solution:
    def search(self, nums: List[int], target: int) -> int:
        low = 0
        high = len(nums) - 1

        if low > high:
            return -1

        while low <= high:

            mid = low + (high-low)//2

            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                high = mid - 1
            else: 
                low = mid + 1
        
        return -1

# Binary Search 
# Time - O(logn)
# Space - O(1)