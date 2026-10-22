# Tries — DSA Interview Notes
*Trie Fundamentals & Implementation · Trie Applications & Patterns*

> **Note:** No sub-topics were given for this one, so it's split into the two groupings that actually matter for interviews: how to build/implement a trie from scratch, and the recurring problem patterns that signal "use a trie."

---

All code examples in Python.

---

## 🔑 Cheat Sheet — Both Sections at a Glance
| Section | Core Idea | Time | Space |
|---|---|---|---|
| Trie Fundamentals | Tree where each path from root spells out a prefix; shared prefixes share nodes | O(L) insert/search, L = word length | O(alphabet × total chars stored) |
| Trie Applications | Combine trie with DFS/backtracking for prefix-aware search over many words at once | Varies — typically O(words × L) or better | O(total chars across all words) |

**Core shared idea:** a trie turns "does any word in this dictionary start with X?" from an O(n × L) scan (check every word) into an O(L) walk down a tree — because all words sharing a prefix physically share the same path from the root.

---

# 1. Trie Fundamentals & Implementation

## 🔑 Cheat Sheet
| Operation | Complexity | Notes |
|---|---|---|
| Insert word | O(L) | L = length of the word |
| Search exact word | O(L) | Must end on a node marked "end of word" |
| Search prefix (`startsWith`) | O(L) | Just needs the path to exist — no "end of word" check |
| Space | O(total characters across all inserted words), shared prefixes reduce this | Each node commonly holds up to 26 children (lowercase English) |

## Core Intuition
A trie (prefix tree) stores strings **character by character**, where each node represents "the path taken so far is a valid prefix." Words that share a prefix (like "cat", "car", "card") **share the same nodes** for that shared prefix, splitting only where the words diverge.

```
Insert: "cat", "car", "card", "dog"

root
├── c
│   └── a
│       ├── t (end of word: "cat")
│       └── r (end of word: "car")
│           └── d (end of word: "card")
└── d
    └── o
        └── g (end of word: "dog")
```
Notice "car" is a **prefix of** "card" and is marked as its own complete word at the `r` node, while the path continues further to spell "card."

### Why This Beats a Hashset of Words for Prefix Queries
A `set` of words gives O(1) exact-match lookup, but answering "does any word start with 'ca'?" requires scanning **every word** in the set — O(n × L). A trie answers the same question in O(L) by just walking down the prefix path once, regardless of how many words are stored.

## Node & Trie Implementation (Python)
```python
class TrieNode:
    def __init__(self):
        self.children = {}       # char -> TrieNode
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end_of_word = True

    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix):
        return self._find_node(prefix) is not None

    def _find_node(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```
**Key idea:** `search` and `startsWith` share almost identical traversal logic — the only difference is whether you additionally check `is_end_of_word` at the destination node. Factoring out `_find_node` avoids duplicating the walk logic.

## Common Pitfalls
- Forgetting the `is_end_of_word` flag — without it, you can't distinguish "car" being a complete word from "car" merely being a prefix of "card." A pure "does this path exist" check isn't enough for `search`.
- Using a fixed-size array (`[None] * 26`) vs. a dict for children — array is faster/more cache-friendly for lowercase-only alphabets, but a dict is more flexible for mixed characters/Unicode. Know both, pick based on the problem's constraints.
- Not handling the empty string or duplicate insertions — inserting the same word twice should be a no-op (still just marks `is_end_of_word = True`, harmless but worth being aware of).

## Interview Talking Points
- Be ready to implement `Trie` (LeetCode 208, "Implement Trie") from memory — it's a very common warm-up/foundation question before moving into trie-based application problems.
- Explicitly state the space trade-off: a trie can use **more** memory than a hashset for a small number of unrelated words (extra node overhead), but wins decisively when many words **share prefixes** or when prefix queries are needed.

---

# 2. Trie Applications & Patterns

## 🔑 Cheat Sheet
| Pattern | Idea |
|---|---|
| Word Search II (grid + word list) | Build a trie of all target words, DFS the grid while walking the trie in lockstep — prune branches the trie says can't lead anywhere |
| Autocomplete / prefix suggestions | Walk to the prefix's node, then DFS/BFS the subtree below it to collect all completions |
| Longest common prefix (of a word list) | Insert all words, walk from root while each node has exactly one child and isn't a word-end |
| Word Dictionary with wildcards (`.` matches any char) | Trie + DFS, branching into **all** children when a wildcard is encountered |
| Replace words with their shortest root (word stemming) | Trie of roots, walk each word until you hit an `is_end_of_word` node — that's the shortest root |

## Signal → Technique
| Signal in Problem Statement | Technique |
|---|---|
| "search a grid of letters for words from a given list" | Trie + DFS/backtracking over the grid, walking the trie alongside grid traversal |
| "design an autocomplete system" | Trie storing all known strings, DFS from the queried-prefix's node to collect completions |
| "does this string match any pattern with wildcards" | Trie + DFS branching on wildcard characters |
| "find the shortest prefix that represents a word" (word stemming/replace) | Trie of prefixes/roots, walk and stop at first `is_end_of_word` |
| "group / count words by shared prefix" | Trie, aggregate counts at nodes during insertion |

## Worked Pattern: Word Search II (Trie + DFS on a grid)
```python
def findWords(board, words):
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end_of_word = True
        node.word = word          # store full word at the terminal node for easy retrieval

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return                          # prune: no word in the trie continues this way
        next_node = node.children[ch]
        if next_node.is_end_of_word:
            result.append(next_node.word)
            next_node.is_end_of_word = False   # avoid duplicate additions

        board[r][c] = '#'                    # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        board[r][c] = ch                     # backtrack: unmark

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return result
```
**Key idea — why the trie matters here:** without it, you'd run a separate DFS from every cell **for every word** in the list — O(words × rows × cols × 4^L). With a shared trie, one DFS pass explores **all words simultaneously**, pruning the instant the current path stops matching *any* word's prefix.

## Common Pitfalls
- Running a fresh DFS per word instead of building one shared trie — defeats the entire point of using a trie for this pattern.
- Forgetting to **backtrack** the visited marker (`board[r][c] = ch` after recursing) — leaves the board corrupted for subsequent searches from other starting cells.
- Not de-duplicating found words when a word could be discovered via multiple paths — clearing `is_end_of_word` after the first match (as shown above) is a simple guard.
- For wildcard search (`.` matches any character), forgetting to branch into **all** children rather than a single specific one when the wildcard is encountered — this turns the DFS into a small combinatorial search at that character position.

## Interview Talking Points
- If a problem involves searching for **multiple words/patterns** against the same text/grid, immediately flag "build one trie, search once" as more efficient than repeating a search per word — this is the core value proposition of tries in interviews.
- For autocomplete-style questions, be ready to discuss how you'd rank/limit suggestions (e.g., top-k by frequency) — often a natural follow-up once basic trie traversal is established.

---

## 📋 Quick Cross-Section Revision Table

| Question to Ask Yourself | If Yes → |
|---|---|
| Do I need fast prefix queries (startsWith) over many strings? | Trie |
| Am I searching for multiple target words against the same text/grid? | Build one shared trie, search once with DFS |
| Do I need to find the shortest prefix/root representation of words? | Trie, stop DFS at first `is_end_of_word` |
| Is the alphabet small and fixed (lowercase letters)? | Consider array-based children (`[None]*26`) over a dict for speed |
| Do I just need exact-match membership, no prefix logic? | A plain hashset is simpler and sufficient — trie is overkill |

## Suggested Problem Set for This Section
- **Fundamentals:** Implement Trie (Prefix Tree)
- **Applications:** Design Add and Search Words Data Structure (wildcard), Word Search II, Longest Word in Dictionary, Replace Words, Design Search Autocomplete System
