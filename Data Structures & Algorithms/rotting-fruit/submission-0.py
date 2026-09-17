class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        q = collections.deque()
        fresh = 0
        time = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    fresh += 1
                if grid[r][c] == 2:
                    q.append((r, c))

        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]

        while fresh > 0 and q:
            length = len(q)
            for i in range(length):
                r, c = q.popleft()

                for dr, dc in directions:
                    if (r+dr in range(rows) and c+dc in range(cols) and grid[r+dr][c+dc] == 1):
                        grid[r+dr][c+dc] = 2
                        q.append((r+dr, c+dc))
                        fresh -= 1

            time += 1

        return time if fresh == 0 else -1

# Time - O(m*n), Space - O(m*n)