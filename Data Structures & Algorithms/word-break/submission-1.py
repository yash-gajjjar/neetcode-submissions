class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        wordset = set(wordDict)

        dp = [False]*(n+1)
        dp[n] = True

        for i in range(n-1, -1, -1):
            
            for word in wordset:
                end = i + len(word)

                if end <= n and s[i:end] == word:
                    dp[i] = dp[end]

                if dp[i]:
                    break

        return dp[0]

# Time - O(n*k*L) , Space - O(n)
# n = len(s), k = number of words in dict, L = max word length