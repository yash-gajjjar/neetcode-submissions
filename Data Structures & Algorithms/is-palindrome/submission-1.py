class Solution:
    def isPalindrome(self, s: str) -> bool:
        chars = []

        for char in s:
            if char.isalnum():
                chars.append(char.lower())

        rev_chars = chars[::-1]

        if chars == rev_chars:
            return True
        
        return False

# BFS

# Time - O(N)
# Space - O(N)