class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        n = len(nums)
        prefix_nums, suffix_nums, new_nums = [1]*(n+1), [1]*(n+1), [1]*n

        for i in range(1, n+1):
            prefix_nums[i] = prefix_nums[i-1]*nums[i-1]

        for i in range(n-1 , -1, -1):
            suffix_nums[i] = suffix_nums[i+1]*nums[i]

        for i in range(n):
            new_nums[i] = prefix_nums[i] * suffix_nums[i+1]

        return new_nums