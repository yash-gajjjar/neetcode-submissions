class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:

        def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
            dummy = ListNode()
            curr = dummy
            while list1 and list2:
                if list1.val < list2.val:
                    curr.next = list1
                    list1 = list1.next
                else:
                    curr.next = list2
                    list2 = list2.next
                curr = curr.next

            if list1:
                curr.next = list1
            else:
                curr.next = list2

            return dummy.next

        def mergeLists(left, right):
            if left > right:
                return None

            if left == right:
                return lists[left]
            
            mid = (left + right) // 2 # Find middle

            left_list = mergeLists(left, mid) # Recursively merge left half

            right_list = mergeLists(mid + 1, right) # Recursively merge right half

            return mergeTwoLists(left_list, right_list) # Merge the two sorted lists

        return mergeLists(0, len(lists) - 1)