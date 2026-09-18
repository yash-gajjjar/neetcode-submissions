class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        preMap = { i: [] for i in range(numCourses)}
        for crs, pre in prerequisites:
            preMap[crs].append(pre)

        visit = set()

        def dfs(crs):
            if crs in visit:
                return False
            if preMap[crs] == []:
                return True

            visit.add(crs)
            for pre in preMap[crs]:
                if not dfs(pre):
                    return False

            visit.remove(crs)
            preMap[crs] = []

            return True

        for cur in range(numCourses):
            if not dfs(cur):
                return False

        return True

# Time - O(c+p), Space - O(c+p) , c = course, p = prerequisites
