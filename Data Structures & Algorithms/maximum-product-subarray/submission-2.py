class Solution:
    
    def maxProduct(self, nums: List[int]) -> int:

        max_product = nums[0]
        left_product = 1
        right_product = 1

        for i in range(len(nums)):

            if left_product == 0:
                left_product = 1
            
            if right_product == 0:
                right_product = 1

            left_product *= nums[i]

            right_product *= nums[len(nums) - 1 - i]

            max_product = max(max_product, right_product, left_product)

        return max_product

# Time - O(N), Space - O(1)