class Solution:
    def longestPalindrome(self, s: str) -> str:

        res = ""
        def expand(left, right):
            nonlocal res
            while left >= 0 and right < len(s) and s[left] == s[right]:
                if right - left + 1 > len(res):
                    res = s[left:right + 1]

                left -= 1
                right += 1

        for i in range(len(s)):
            # Odd-length palindrome
            expand(i, i)
            # Even-length palindrome
            expand(i, i + 1)

        return res

# Time - O(N^2), Space - O(1)