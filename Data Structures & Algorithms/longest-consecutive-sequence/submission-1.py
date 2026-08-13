class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0

        num_set = set(nums)
        max_count = 0

        for num in num_set:
            if num-1 not in num_set:
                current_num = num
                current_streak = 1

                while current_num+1 in num_set:
                    current_num += 1
                    current_streak += 1

                max_count = max(max_count, current_streak)

        return max_count



# Optimize 

# Time  = O(n)
# Space = O(1)
        
        