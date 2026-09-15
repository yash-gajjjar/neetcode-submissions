class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []

        def valid(s):
            open = 0
            for c in s:
                if c == '(':
                    open += 1
                else:
                    open -= 1
                if open < 0:
                    return False
            return not open

        def dfs(s):
            if n * 2 == len(s):
                if valid(s):
                    res.append(s)
                return 
            
            dfs(s + '(')
            dfs(s + ')')

        dfs('')
        return res

# Time = O(n × 4^n) , Space = O(n × Cₙ), Cₙ) Catalan number
            