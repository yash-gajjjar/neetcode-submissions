class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        subset = []

        def backtrack():
            if len(subset) == len(nums):
                res.append(subset.copy())
                return

            for num in nums:
                if num not in subset:
                    subset.append(num)
                    backtrack()
                    subset.pop()

        backtrack()
        return res

# Time - O(N × N!), Space - O(N × N!)