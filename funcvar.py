full_txt = ''
word = ''
valid_word = True

def update_word(ch):
    global full_txt, word, valid_word
    
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