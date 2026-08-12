class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hashmap = {}

        for words in strs:
            key = "".join(sorted(words))
            if key in hashmap:
                hashmap[key].append(words)
            else:
                hashmap[key] = [words]

        return list(hashmap.values())