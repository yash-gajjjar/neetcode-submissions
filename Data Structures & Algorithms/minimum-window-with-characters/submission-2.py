
from collections import Counter
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t or len(t) > len(s):
            return ""

        # 1. Store the required frequency of each character in t
        need = Counter(t)

        # 2. Track the frequency of characters in the current window
        window = {}

        left, formed = 0, 0
        required = len(need)

        min_len = float("inf")
        start = 0

        # 3. Expand the window using the right pointer
        for right in range(len(s)):
            char = s[right]

            if char in need:
                window[char] = window.get(char, 0) + 1

                # Character has reached its required frequency
                if window[char] == need[char]:
                    formed += 1

            # 4. Shrink the window while it remains valid
            while formed == required:
                # Update the minimum window
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    start = left

                left_char = s[left]

                if left_char in need:
                    # Removing this character may make the window invalid
                    if window[left_char] == need[left_char]:
                        formed -= 1

                    window[left_char] -= 1

                left += 1

        # 5. Return the minimum valid substring
        if min_len == float("inf"):
            return ""

        return s[start:start + min_len]
