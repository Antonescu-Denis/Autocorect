import wordfreq, Levenshtein, os


full_txt = ''
word = ''
valid_word = True
max_predict = 5
min_length = 3
max_candidate = 100
suggestions = ['' for _ in range(max_predict)]
candidates = []
wordlist = []

def update_word(ch):
    global full_txt, word, valid_word, suggestions
    
    if ch == ' ':
        word = ''
        full_txt += ch
        valid_word = True
    elif ch == 'del' and len(full_txt) > 0:
        full_txt = full_txt[:-1]
        word = full_txt[full_txt.rfind(' ')+1:]
        if not word.isalpha() or not word.isascii():
            valid_word = False
    elif ch == 'ent':
        full_txt = ''
        word = ''
    else:
        full_txt += ch
        if ch.isalpha() and ch.isascii():
            if valid_word:
               word += ch
        else:
            valid_word = False

    if not valid_word:
        word = ''

    suggestions = [word for _ in range(max_predict)]

def match_caps(og, ref):
    temp = ''
    for i in range(len(og)):
        if og[i].islower():
            temp += ref[i].lower()
        else:
            temp += ref[i].upper()
    return temp

def get_word_list():
    global wordlist

    n = 0
    for thing in wordfreq.get_frequency_list('ro'):
        for word in thing:
            if word.isalpha() and len(word) >= min_length:
                wordlist.append(word)
                n += 1
    wordlist.sort()
    
    path = os.path.realpath(__file__)
    path = path[:path.rfind('\\')+1]
    if not os.path.exists(path+'wordlist.txt'):
        with open(path+'wordlist.txt', 'w', encoding = 'utf-8') as file:
            for word in wordlist:
                #try:
                #    file.write(word+'\n')
                #except Exception:
                #    print(f":{word}:")
                file.write(word+'\n')
    else:
        with open(path+'wordlist.txt', 'r', encoding = 'utf-8') as file:
            pass

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
    if main == None:
        return
    for key, val in main.branch.items():
        if val != None:
            select_candidates(val, word+key)
        else:
            candidates.append(word)