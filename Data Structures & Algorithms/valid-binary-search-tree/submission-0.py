class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        def dfs(node, minVal, maxVal):
            if not node:
                return True

            if node.val <= minVal or node.val >= maxVal:
                return False

            return (
                dfs(node.left, minVal, node.val)
                and dfs(node.right, node.val, maxVal)
            )

        return dfs(root, float("-inf"), float("inf"))

# DFS
# Time  → O(N)
# Space → O(H)