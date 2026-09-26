class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        dp = {}

        def dfs(r, c, prevVal):
            if (min(r, c) < 0 or r >= rows or c >= cols 
                    or matrix[r][c] <= prevVal):
                return 0

            if (r, c) in dp:
                return dp[(r,c)]

            res = 1
            for d in directions:
                res = max(res, 1 + dfs(r + d[0], c + d[1], matrix[r][c]))
            dp[(r,c)] = res
            return res

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, -1)
        return max(dp.values())

# Time - O(m*n), Space - O(m*n)