class Solution:
    def rob(self, nums: List[int]) -> int:

        if len(nums) == 1:
            return nums[0]

        def rob_linear(nums):
            nums = nums.copy()
            nums.append(0)

            n = len(nums)

            for i in range(n - 3, -1, -1):
                nums[i] = max(nums[i+1], nums[i] + nums[i + 2])

            return max(nums[0], nums[1])

        case1 = rob_linear(nums[:-1])
        case2 = rob_linear(nums[1:])

        return max(case1, case2)

# Time - O(N) , Space - O(N)