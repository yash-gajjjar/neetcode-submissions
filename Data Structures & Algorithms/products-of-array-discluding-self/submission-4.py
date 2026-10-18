
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        product, zero_count = 1, 0

        for num in nums:
            if num == 0:
                zero_count += 1
            else:
                product *= num

        if zero_count >= 2:
            return [0] * len(nums)

        result = []

        for num in nums:
            if zero_count == 1:
                if num == 0:
                    result.append(product)
                else:
                    result.append(0)
            else:
                result.append(product // num)

        return result
