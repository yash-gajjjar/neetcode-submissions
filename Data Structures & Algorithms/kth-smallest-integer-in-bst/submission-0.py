class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        count = 0
        result = 0

        def dfs(node):
            nonlocal count, result

            if not node:
                return

            dfs(node.left)

            count += 1

            if count == k:
                result = node.val
                return

            dfs(node.right)

        dfs(root)

        return result

# BFS
# Time  - O(H + K) average traversal until kth node
# Space - O(H)