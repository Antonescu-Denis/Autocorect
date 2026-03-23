full_txt = ''
word = ''
valid_word = True
max_predict = 5
suggestions = ['' for _ in range(max_predict)]

def update_word(ch):
    global full_txt, word, valid_word, suggestions
    
    full_txt += ch
    if ch == ' ':
        word = ''
        valid_word = True
    elif ch == 'del' and len(full_txt) > 0:
        full_txt = full_txt[:-1]
        word = full_txt[full_txt.rfind(' ')+1:]
        if not word.isalpha():
            valid_word = False
            word = ''
    elif ch == 'ent':
        full_txt = ''
        word = ''
    elif ch.isalpha() and valid_word:
        word += ch
    else:
        word = ''
        valid_word = False

    suggestions = [word for _ in range(max_predict)]