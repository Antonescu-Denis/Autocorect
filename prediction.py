import wordfreq, Levenshtein
import funcvar as fv


class Tree:
    char = '-'
    branch = {}

    def __init__(self, char):
        self.char = char
        self.branch = {}

    def add_word(self, word):
        curr = self
        i = 0
        while i < len(word):
            if word[i] not in curr.branch.keys():
                curr.branch[word[i]] = Tree(word[i])
            curr = curr.branch[word[i]]
            i += 1
        curr.branch['_'] = None

def print_tree(main, spacing = ''):
    if main == None:
        return
    for key, val in main.branch.items():
        print(f"{spacing}- {key}")
        print_tree(val, spacing+'  ')

def find_start(main, word):
    head = main
    i = 0
    while i < len(word):
        if word[i] in head.branch.keys():
            head = head.branch[word[i]]
            i += 1
        else:
            i = -1
            break
    if i != -1:
        #print(f":{head.char} - {head.branch}:")
        select_candidates(head)

def select_candidates(main, word = ''):
    global candidates
    if main == None:
        return
    for key, val in main.branch.items():
        if val != None:
            select_candidates(val, word+key)
        else:
            candidates.append(word)

root = Tree('-')
candidates = []
filtered = []

for char in wordfreq.get_frequency_list('ro'):
    for th in char:
        if th.isalpha() and len(th) > 2:
            filtered.append(th)
filtered.sort()

for char in filtered[:10]:
    root.add_word(char)
print_tree(root)
print()
find_start(root, 'abandon')


# don't make suggestions until len(fv.word) == min_length
# suggestions should have same/greater length than fv.word
# make trie for words, each node has:
#     - end of word flag
#     - dict of chars and their nodes
# maybe stop when you have enough suggestions, or adjust at runtime
#     - optional but ideal, pre-sort words by frequency 
# store trie somehow for performance
# word ranking:
#     - frequency, more frequent = better
#     - edit distance, smaller edit distance = better