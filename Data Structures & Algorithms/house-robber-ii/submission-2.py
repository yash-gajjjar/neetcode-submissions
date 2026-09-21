class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def rob_linear(nums):
            rob1 = 0
            rob2 = 0

            for num in nums:
                temp = max(num + rob1, rob2)
                rob1 = rob2
                rob2 = temp

            return rob2

        return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))

# Time - O(N) , Space - O(1)