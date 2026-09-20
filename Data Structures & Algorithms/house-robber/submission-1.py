class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        rob1 = 0
        rob2  = 0

        for num in nums:
            temp = max(num+rob1, rob2)
            rob1 = rob2
            rob2 = temp

        return max(rob1, rob2)

# Time - O(N), Space - O(1)
