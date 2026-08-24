class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        visible = set()
        for num in nums:
            if num in visible:
                return num
            visible.add(num)
        return -1


# BFS
# Time - O(n) , Space - O(n)