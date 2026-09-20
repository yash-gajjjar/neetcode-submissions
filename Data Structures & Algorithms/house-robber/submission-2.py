class Solution:
    def rob(self, nums: List[int]) -> int:
        prev2 = 0
        prev1 = 0

        for num in nums:
            current = max(
                num + prev2,  # Rob current house
                prev1         # Skip current house
            )

            prev2 = prev1
            prev1 = current

        return prev1

# Time - O(N), Space - O(1)
