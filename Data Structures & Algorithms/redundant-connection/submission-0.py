class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:

        adj = {i: [] for i in range(1, len(edges) + 1)}

        def dfs(i, target, visit):
            if i == target:
                return True

            visit.add(i)

            for nei in adj[i]:
                if nei not in visit:
                    if dfs(nei, target, visit):
                        return True

            return False

        for n1, n2 in edges:
            visit = set()

            if dfs(n1, n2, visit):
                return [n1, n2]

            adj[n1].append(n2)
            adj[n2].append(n1)

# Time - O(N^2), Space - O(N)
