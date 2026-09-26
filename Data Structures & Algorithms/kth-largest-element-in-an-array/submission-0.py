class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        sort_nums = sorted(nums)
        return sort_nums[n-k]

# Time - O(nlogn), Space - O(n)