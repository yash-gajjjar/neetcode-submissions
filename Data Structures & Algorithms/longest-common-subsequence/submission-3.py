class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:

        visit = {}
        def dfs(i, j):
            if i == len(text1) or j == len(text2):
                return 0
            if (i, j) in visit:
                return visit[(i, j)]

            if text1[i] == text2[j]:
                visit[(i, j)] = 1 + dfs(i+1, j+1)

            else:
                visit[(i, j)] = max(dfs(i + 1, j), dfs(i, j + 1))

            return visit[(i, j)]

        return dfs(0, 0)

# Memoization - Top-Down - DP
# Time - O(m*n) , Space - O(m*n)