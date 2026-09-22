class Solution:
    def numDecodings(self, s: str) -> int:

        visit = {}
        
        def dfs(i):
            if i == len(s):
                return 1

            if s[i] == '0':
                return 0
                
            if i in visit:
                return visit[i]

            # take 1 digit
            count = dfs(i+1)

            # take 2 digit
            if i+1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
                count += dfs(i+2)

            visit[i] = count
            return count

        return dfs(0)

# Time - O(N) , Space - O(N)
            