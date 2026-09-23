class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        wordset = set(wordDict)

        dp = [False]*(n+1)
        dp[0] = True

        for i in range(n):
            if not dp[i]:
                continue

            for word in wordset:
                end = i + len(word)

                if end <= n and s[i:end] == word:
                    dp[end] = True

        return dp[n]

# Time - O(n*k*L) , Space - O(n+k)
# n = len(s), k = number of words in dict, L = max word length