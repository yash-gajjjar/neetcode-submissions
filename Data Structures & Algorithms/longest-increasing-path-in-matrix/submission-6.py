class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:


        rows, cols = len(matrix), len(matrix[0])
        if rows == 1 and cols == 1:
            return 1
        dp = {}

        def dfs(r, c, prevVal):
            if (min(r, c) < 0 or r >= rows or c >= cols 
                    or matrix[r][c] <= prevVal):
                return 0

            if (r, c) in dp:
                return dp[(r,c)]

            res = 1
            res = max(res, 1 + dfs(r + 1, c, matrix[r][c]))
            res = max(res, 1 + dfs(r - 1, c, matrix[r][c]))
            res = max(res, 1 + dfs(r, c + 1, matrix[r][c]))
            res = max(res, 1 + dfs(r, c - 1, matrix[r][c]))
            dp[(r,c)] = res
            return res

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, -1)
        return max(dp.values())

# Time - O(m*n), Space - O(m*n)