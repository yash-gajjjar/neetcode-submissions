class Solution:
    def findMin(self, nums: List[int]) -> int:
        
        low = 0
        high = len(nums) - 1

        while low < high:
            mid = low + (high-low)//2

            if nums[mid] > nums[high]:
                low = mid+1 # low point will be on right side
            else:
                high = mid # what is mid is low so don't do (mid - 1)

        return nums[low]

# Binary Search

# Time - O(logn), space = O(1)