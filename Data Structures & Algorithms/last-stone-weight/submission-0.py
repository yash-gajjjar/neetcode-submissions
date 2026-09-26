class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:

        while len(stones) > 1:
            stones.sort()

            p = stones.pop()      # heaviest
            q = stones.pop()      # second heaviest

            if p != q:
                stones.append(p - q)

        return stones[0] if stones else 0

# Time - O(nlogn), Space - O(n)