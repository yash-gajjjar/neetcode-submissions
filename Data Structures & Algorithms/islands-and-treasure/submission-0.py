class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        if not grid:
            return []

        rows, cols = len(grid), len(grid[0])
        q = collections.deque()
        directions = [[1,0], [-1,0], [0,1], [0,-1]]

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0:
                    q.append((r, c))

        while q:
            r, c = q.popleft()

            for dr, dc in directions:
                if r + dr < 0 or r + dr >= rows or c + dc < 0 or c + dc >= cols:
                    continue

                if grid[r + dr][c + dc] != 2147483647:
                    continue

                grid[r + dr][c + dc] = grid[r][c] + 1

                q.append((r + dr, c + dc))

        return

# Time - O(m × n), Space - O(1)