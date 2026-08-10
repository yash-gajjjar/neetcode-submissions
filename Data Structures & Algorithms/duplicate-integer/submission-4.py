class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        hashmap = {}

        for num in nums:
            if num not in hashmap.keys():
                hashmap[num] = 1
            else:
                return True
                
        return False


# Optimal Solution