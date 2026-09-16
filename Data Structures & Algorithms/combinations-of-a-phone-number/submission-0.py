class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        digits_map = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
    }

        if not digits:
            return []

        res = []
        path = []

        def backtrack(index):
            if index == len(digits):
                res.append(''.join(path))
                return 

            for char in digits_map[digits[index]]:
                path.append(char)
                backtrack(index + 1)
                path.pop()

        backtrack(0)
        return res  

# Time - O(N * 4^N), Space - O(N * 4^N)     
