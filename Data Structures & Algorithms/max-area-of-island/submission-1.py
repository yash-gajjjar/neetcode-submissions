class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0

        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        rows, cols = len(grid), len(grid[0])
        max_area = 0

        def dfs(r, c):
            if (r < 0 or c < 0 or r >= rows or
                c >= cols or grid[r][c] == 0):
                return 0

            grid[r][c] = 0
            
            return (1 + dfs(r + 1, c) + 
                        dfs(r - 1, c) + 
                        dfs(r, c + 1) + 
                        dfs(r, c - 1))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    island_area = dfs(r, c)
                    max_area = max(max_area, island_area)

        return max_area

# DFS
# Time - O(r*c), Space - O(r*c)