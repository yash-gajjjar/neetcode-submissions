class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        prev1 = 2
        prev2 = 1

        for i in range(3, n+1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr

        return prev1

# Time - O(n), Space - O(1)