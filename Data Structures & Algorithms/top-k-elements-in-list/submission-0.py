class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        hashmap = {}
        new_nums = []

        for num in nums:
            if num in hashmap:
                hashmap[num] += 1
            else:
                hashmap[num] = 1

        desc_dict = dict(sorted(hashmap.items(), key=lambda item: item[1], reverse=True)[:k])  

        for element in desc_dict.keys():
            new_nums.append(element)  

        return new_nums  


