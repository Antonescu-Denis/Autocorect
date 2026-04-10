full_txt = ''
word = ''
valid_word = True
max_predict = 5
min_length = 3
suggestions = ['' for _ in range(max_predict)]

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