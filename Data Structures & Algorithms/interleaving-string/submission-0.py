class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:

        if not len(s3) == len(s1) + len(s2):
            return False

        n = len(s1)
        m = len(s2)

        dp = [[False] * (m+1) for _ in range(n+1)]

        dp[0][0] = True

        for i in range(n + 1):
            for j in range(m + 1):
                # Take character from s1
                if i > 0 and s1[i-1] == s3[i+j-1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]

                # Take character from s2
                if j > 0 and s2[j-1] == s3[i+j-1]:
                    dp[i][j] = dp[i][j] or dp[i][j-1]

        return dp[n][m] 

# Time - O(n*m), Space - O(n*m)
