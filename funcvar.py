import wordfreq, os
import Levenshtein as lev


full_txt = ''
main_word = ''
valid_word = True
max_predict = 5
min_length = 2
max_diff = 0.65
max_distance = 5
max_candidates = 100
curr_candidates = 0
suggestions = ['-' for _ in range(max_predict)]
candidates = {}
caps = ''

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

def is_word_valid():
    global main_word

    if len(full_txt) == 0:
        return True

    if len(main_word) > 0 and main_word.isalpha():
        diacritics = False
        for ch in 'ĂăÂâÎîȘșȚț':
            if ch in main_word:
                diacritics = True
                break
        if main_word.isascii():
            return True
        else:
            if diacritics:
                return True
            else:
                return False
    else:
        return False

def update_word(ch):
    global full_txt, main_word, valid_word, root, caps
    
    if ch == ' ':
        reset_word()
        full_txt += ch
        valid_word = True
    elif ch == 'del':
        if len(full_txt) > 0:
            full_txt = full_txt[:-1]
            caps = full_txt[full_txt.rfind(' ')+1:]
            main_word = caps.lower()
            valid_word = is_word_valid()
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

def get_words():
    global candidates

    if os.path.exists('wordlist.txt'):
        get_word_list_file()
    else:
        get_word_list()
    i = 1.00
    while i > 0:
        i = round(i, 2)
        candidates[i] = []
        i -= 0.01

def get_word_list():
    global root
    
    english = set()
    for thing in wordfreq.get_frequency_list('en', wordlist = 'large'):
        for word in thing:
            if len(word) >= min_length and word.isalpha():
                english.add(word)
    
    w_diacritics = []
    wo_diacritics = []
    for thing in wordfreq.get_frequency_list('ro'):
        for word in thing:
            if len(word) >= min_length and word.isalpha():
                diacritics = False
                for ch in 'ĂăÂâÎîȘșȚț':
                    if ch in word:
                        diacritics = True
                        break
                if word.isascii():
                    if word not in english:
                        if diacritics:
                            w_diacritics.append(word)
                        else:
                            wo_diacritics.append(word)
                else:
                    if diacritics:
                        if word not in english:
                            w_diacritics.append(word)
    romanian = w_diacritics + wo_diacritics

    with open('wordlist.txt', 'w', encoding = 'utf-8') as file:
        for word in romanian:
            file.write(word+'\n')
            root.add_word(word)
    print(f"new: {len(romanian)}")

def get_word_list_file():
    global root
    
    with open('wordlist.txt', 'r', encoding = 'utf-8') as file:
        for word in file:
            word = word.strip()
            root.add_word(word)

def print_tree(main, spacing = '    '):
    if main == None:
        return
    for key, val in main.branch.items():
        print(f"{spacing}- {key}")
        print_tree(val, spacing+'    ')

def search_root(main, word):
    global curr_candidates

    curr_candidates = 0
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
    global candidates, max_candidates, curr_candidates

    if main == None:
        return
    for key, val in main.branch.items():
        if curr_candidates <= max_candidates:
            if val != None:
                select_candidates(val, word+key)
            else:
                ratio = lev.ratio(main_word, word)
                candidates[round(ratio, 2)].append(word)
                curr_candidates += 1
        else:
            break

def get_typos(main, word = ''):
    global candidates, max_candidates, curr_candidates, main_word, max_diff, max_distance

    if main == None or curr_candidates > max_candidates:
        return
    for key, val in main.branch.items():
        if curr_candidates <= max_candidates:
            if val != None:
                get_typos(val, word+key)
            else:
                if len(word+key) >= len(main_word):
                    ratio = lev.ratio(main_word, word)
                    if ratio >= max_diff and lev.distance(main_word, word) <= max_distance:
                        candidates[round(ratio, 2)].append(word)
                        curr_candidates += 1
        else:
            break

def update_candidates():
    global root, main_word, candidates, min_length, suggestions, typos
    
    for key in candidates.keys():
        candidates[key] = []
    suggestions = []
    if len(main_word) >= min_length:
        search_root(root, main_word)
        get_typos(root)

        nums = 0
        for key, val in candidates.items():
            for word in val:
                suggestions.append(word)
                nums += 1
                if nums >= max_predict:
                    break
            if nums >= max_predict:
                break

        while len(suggestions) < max_predict:
            suggestions.append('-')
    else:
        suggestions = ['-' for _ in range(max_predict)]