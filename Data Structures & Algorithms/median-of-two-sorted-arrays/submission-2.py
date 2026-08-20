class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged_arr = []
        i, j = 0, 0

        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                merged_arr.append(nums1[i])
                i += 1
            else: 
                merged_arr.append(nums2[j])
                j += 1

        while i < len(nums1):
            merged_arr.append(nums1[i])
            i += 1
        while j < len(nums2):
            merged_arr.append(nums2[j])
            j += 1

        if len(merged_arr) % 2 == 1:
            median = merged_arr[len(merged_arr) // 2]
        else:
            mid = len(merged_arr) // 2
            median = (merged_arr[mid - 1] + merged_arr[mid]) / 2

        return median


# Time - O(M + N), Space - O(M + N)