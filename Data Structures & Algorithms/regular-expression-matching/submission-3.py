class Solution:
    def isMatch(self, s: str, p: str) -> bool:

        n, m = len(s), len(p)
        dp = {}

        def dfs(i, j):
            # patten completly consume
            if j == m:
                return i == n

            if (i, j) in dp:
                return dp[(i, j)]

            # check for current char
            first_match = (i < n and (s[i] == p[j] or p[j] == '.'))

            # curr char. followed by star
            if j + 1 < m and p[j + 1] == '*':
                # use zero occurance or consume one char
                dp[(i, j)] = (dfs(i, j + 2) or (first_match and dfs(i + 1, j)))
                return dp[(i, j)]
            
            if first_match:
                dp[(i, j)] = dfs(i + 1, j + 1)
                return dp[(i, j)]
            
            dp[(i, j)] = False
            return False

        return dfs(0, 0)

# Time - O(n*m) , Space - O(n*m)