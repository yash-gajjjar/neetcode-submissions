class Solution:
    def rob(self, nums: List[int]) -> int:
        nums.append(0)
        n = len(nums)

        for i in range(n-3, -1, -1):
            nums[i] = max(nums[i+1], nums[i] + nums[i+2])

        return max(nums[0], nums[1])

# Time - O(N), Space - O(1)
