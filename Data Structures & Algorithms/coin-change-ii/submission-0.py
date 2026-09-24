class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
         
        visit = {}
        def dfs(i , amount):
            if amount == 0:
                return 1

            if i == len(coins):
                return 0

            if (i, amount) in visit:
                return visit[(i, amount)]

            # don't take current coin
            skip = dfs(i+1, amount)

            # take current coin
            take = 0
            if coins[i] <= amount:
                take = dfs(i, amount - coins[i])

            visit[(i, amount)] = skip + take            

            return visit[(i, amount)]

        return dfs(0, amount)

# Time - O(N*t), Space - O(t) 
# Top - bottom - Memoization (Visit = {})