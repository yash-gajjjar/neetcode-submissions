class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        
        def dfs(p, q):
            if not p and not q:
                return True

            if not p or not q:
                return False
                
            if p.val != q.val:
                return False

            return dfs(p.left, q.left) and dfs(p.right, q.right)

        return dfs(p, q) 

# DFS
# Time - O(N)
# Space - O(h), Best - O(logN), worst - O(N)       