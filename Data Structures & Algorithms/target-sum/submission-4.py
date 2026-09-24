class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
      
        dp = {}  # (i, target) -> value
        
        def dfs(i, total):
            if (i, total) in dp:
                return dp[(i, total)]

            if i == len(nums):
                return 1 if total == target else 0

            # case1 - Add nums[i]
            dp[(i, total)] = (dfs(i+1, total + nums[i]) + dfs(i+1, total - nums[i]))

            return dp[(i, total)]

        return dfs(0, 0)