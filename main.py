from pynput import keyboard as kb
from pynput import mouse
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

def mouse_click(x, y, button, pressed):
    print(f"{'Pressed' if pressed else 'Released'}  at {(x, y)}")
    if not pressed:
        return False

#kb_listen = kb.Listener(on_press = key_press)
#kb_listen.start()
#kb_listen.join()
mouse_listen = mouse.Listener(on_click = mouse_click)
mouse_listen.start()
mouse_listen.join()