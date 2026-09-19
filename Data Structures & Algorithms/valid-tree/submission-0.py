class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if not n:
            return True

        adj = { i:[] for i in range(n)}

        for n1, n2 in edges:
            adj[n1].append(n2)
            adj[n2].append(n1)

        visit = set()
        def dfs(i, prev):
            if i in visit:
                return False
            visit.add(i)
            
            for nei in adj[i]:
                if nei == prev:
                    continue

                if not dfs(nei, i):
                    return False

            return True

        return dfs(0, -1) and n == len(visit)

# Time - O(node + edge), Space - O(node + edge)

    