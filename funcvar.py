import wordfreq, Levenshtein, os


full_txt = ''
main_word = ''
valid_word = True
max_predict = 5
min_length = 3
max_candidate = 100
suggestions = ['-' for _ in range(max_predict)]
candidates = []
wordlist = []
caps = ''
typing = False

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
        curr.branch['!'] = None
root = Tree('-')


def reset_word():
    global caps, main_word

    main_word = ''
    caps = ''

def update_word(ch):
    global full_txt, main_word, valid_word, suggestions, root, caps
    
    if ch == ' ':
        reset_word()
        full_txt += ch
        valid_word = True
    elif ch == 'del':
        if len(full_txt) > 0:
            full_txt = full_txt[:-1]
            caps = full_txt[full_txt.rfind(' ')+1:]
            main_word = caps.lower()
            if len(main_word) > 0 and (not main_word.isalpha() or not main_word.isascii()):
                valid_word = False
    elif ch == 'ent':
        full_txt = ''
        reset_word()
    else:
        full_txt += ch
        if ch.isalpha() and ch.isascii():
            if valid_word:
               caps += ch
               main_word += ch.lower()
        else:
            valid_word = False

    if not valid_word:
        reset_word()

    print(f"full text: |{full_txt}|\nword: |{main_word}|\ncaps: {caps}\nvalid: {valid_word}\n")

def match_caps(ref):
    global caps

    temp = ''
    caps_len = len(caps)
    for i in range(len(ref)):
        if i < caps_len:
            if caps[i].islower():
                temp += ref[i].lower()
            else:
                temp += ref[i].upper()
        else:
            temp += ref[caps_len:]
            break
    return temp

def get_word_list():
    global wordlist, root
    
    for thing in wordfreq.get_frequency_list('ro'):
        for word in thing:
            if word.isalpha() and len(word) >= min_length:
                wordlist.append(word)
                root.add_word(word)

def print_tree(main, spacing = '    '):
    if main == None:
        return
    for key, val in main.branch.items():
        print(f"{spacing}- {key}")
        print_tree(val, spacing+'    ')

def search_root(main, word):
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
        select_candidates(head, word)

def select_candidates(main, word = ''):
    global candidates

    if main == None:
        return
    for key, val in main.branch.items():
        if val != None:
            select_candidates(val, word+key)
        else:
            candidates.append(word)

def update_candidates():
    global root, main_word, candidates, min_length, suggestions
    
    if len(main_word) >= min_length:
        candidates = []
        search_root(root, main_word)
        suggestions = candidates[:min(len(candidates), max_predict)]
        while len(suggestions) < max_predict:
            suggestions.append('-')
    else:
        candidates = []
        suggestions = ['-' for _ in range(max_predict)]


# word ranking:
#     - frequency, more frequent = better
#     - edit distance, smaller edit distance = better
#thing = 'ĂăÂâÎîȘșȚț'