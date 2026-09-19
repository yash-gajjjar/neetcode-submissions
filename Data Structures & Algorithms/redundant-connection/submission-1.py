class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # parent array: parent[i] points to the representative of node i's set
        # Initially, each node is its own parent (1-indexed)
        parent = [i for i in range(len(edges) + 1)]
        
        # rank array: helps keep trees balanced during union operations
        rank = [1] * (len(edges) + 1)

        def find(n):
            # Find the root representative of node n
            p = parent[n]
            while p != parent[p]:
                # Path Compression: flatten the tree structure for faster future lookups
                parent[p] = parent[parent[p]]
                p = parent[p]
            return p

        def union(n1, n2):
            # Find the root parents of both nodes
            p1, p2 = find(n1), find(n2)
            
            # If they already share the same root, an edge between them creates a cycle!
            if p1 == p2:
                return False
            
            # Union by Rank: attach the smaller tree under the root of the larger tree
            if rank[p1] > rank[p2]:
                parent[p2] = p1
                rank[p1] += rank[p2]
            else:
                parent[p1] = p2
                rank[p2] += rank[p1]
            return True

        # Process each edge
        for n1, n2 in edges:
            if not union(n1, n2):
                return [n1, n2]


# Just testing - Need to understand and solved by myself