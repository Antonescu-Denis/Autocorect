from pynput import keyboard as kb
from pynput.keyboard import Key
import wordfreq, Levenshtein


def key_press(key):
    if key in [Key.esc, Key.space, Key.enter]:
        print()
    else:
        k = ''
        try:
            if key.char.isalpha():
                k = key.char
            else:
                k = '-'
        except:
            k = '---'
        print(k)

#kb_listen = kb.Listener(on_press = key_press)
#kb_listen.start()
#kb_listen.join()