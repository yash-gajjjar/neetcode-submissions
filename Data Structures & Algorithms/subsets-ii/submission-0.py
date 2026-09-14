class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res = []
        subset = []

        def backtrack(i):
            if i == len(nums):
                res.append(subset.copy())
                return

            # add element
            subset.append(nums[i])
            backtrack(i+1)
            subset.pop()

            # skip duplicate
            while i + 1 < len(nums) and nums[i] == nums[i+1]:
                i += 1

            backtrack(i+1)

        backtrack(0)
        return res

# Time - O(n*2^n), Space - O(n*2^n)