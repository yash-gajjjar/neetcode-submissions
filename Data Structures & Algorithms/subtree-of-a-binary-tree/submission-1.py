class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def serilize(node):
            if not node:
                return "#"
            
            return (',' + str(node.val) + serilize(node.left) + serilize(node.right))

        root_str = serilize(root)
        subroot_str = serilize(subRoot)

        # KMP preprocessing
        def build_lps(pattern):
            lps = [0] * len(pattern)
            length = 0
            i = 1

            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                elif length > 0:
                    length = lps[length - 1]
                else:
                    i += 1

            return lps

        # kmp search
        def kmp_search(text, pattern):
            lps = build_lps(pattern)

            i = 0  # text pointer
            j = 0  # pattern pointer

            while i < len(text):
                if text[i] == pattern[j]:
                    i += 1
                    j += 1

                    if j == len(pattern):
                        return True

                elif j > 0:
                    j = lps[j - 1]

                else:
                    i += 1

            return False

        return kmp_search(root_str, subroot_str)

# Time - O(N+M), Space - O(N+M)
