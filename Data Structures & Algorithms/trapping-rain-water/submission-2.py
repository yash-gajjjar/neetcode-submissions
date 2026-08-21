class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0
        n = len(height)
        maxleft = [0]*n
        maxright= [0]*n
        res = 0

        maxleft[0] =  0
        for i in range(1,n):
            maxleft[i] =  max(maxleft[i-1], height[i-1])

        maxright[n-1] =  0
        for i in range(n-2,-1,-1):
            maxright[i] =  max(maxright[i+1], height[i+1])

        for i in range(n):
            water = min(maxleft[i] , maxright[i]) - height[i]
            if water > 0:
                res += water
                
        return res

# Test latency with edge case