class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        count1 = {}
        for c in s1:
            count1[c] = 1 + count1.get(c, 0)
        need = len(count1)
        for i in range(len(s2)):
            count2, cur = {}, 0
            for j in range(i, len(s2)):
                count2[s2[j]] = 1 + count2.get(s2[j], 0)
                if s2[j] not in count1:
                    break
                if count2[s2[j]] > count1[s2[j]]:
                    break
                if count2[s2[j]] == count1[s2[j]]:
                    cur += 1
                if cur == need:
                    return True
        return False

# not in count1 → wrong character → BREAK
# count2 > count1 → too many characters → BREAK
# count2 == count1 → this character is perfectly matched → continue