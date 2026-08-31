class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0
        
        def dfs(node):
            if not node:
                return 0

            left = dfs(node.left)
            right = dfs(node.right)

            nonlocal diameter   # This is global parameter 
            diameter = max(diameter, left + right)
            return 1 + max(left, right)

        dfs(root)
        return diameter

# DFS
# Time - O(N)
# Space - O(h), Best - O(logN), worst - O(N)

