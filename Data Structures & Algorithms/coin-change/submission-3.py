class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        
        visit = {}
        def dfs(amount):
            if amount == 0:
                return 0

            if amount in visit:
                return visit[amount]

            res = 1e9

            for coin in coins:
                if amount - coin >= 0:
                    res = min(res, 1 + dfs(amount - coin))
            
            visit[amount] = res
            return res

        minCoins = dfs(amount)

        return -1 if minCoins >= 1e9 else minCoins

# Time - O(N*t), Space - O(t) 
# Top - bottom - Memoization (Visit = {})