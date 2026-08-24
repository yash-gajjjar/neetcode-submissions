class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        visible = set()
        for num in nums:
            if num in visible:
                return num
            visible.add(num)


# BFS
# Time - O(n) , Space - O(n)