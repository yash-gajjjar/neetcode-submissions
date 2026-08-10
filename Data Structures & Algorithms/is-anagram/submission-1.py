class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_hashmap = {}
        t_hashmap = {}

        for char in s:
            if char in s_hashmap:
                s_hashmap[char] += 1
            else:
                s_hashmap[char] = 1

        for char in t:
            if char in t_hashmap:
                t_hashmap[char] += 1
            else:
                t_hashmap[char] = 1

        if s_hashmap == t_hashmap:
            return True
        
        return False



# Time Complexity: O(n + m)
# Space Complexity: O(1) (or O(k), where k is the alphabet size)