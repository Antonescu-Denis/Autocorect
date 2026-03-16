from pynput.keyboard import Key
from pynput import keyboard as kb
from pynput import mouse as m
import funcvar as fv


def key_press(key):
    if key == Key.space:
        fv.update_word(' ')
    elif key == Key.backspace:
        fv.update_word('del')
    elif key == Key.enter:
        fv.update_word('ent')
    else:
        try:
            if key.char:
                fv.update_word(key.char)
        except Exception:
            pass
    print(f"full: {fv.full_txt}\n    last word: {fv.word}\n")

def left_click(x, y, button, pressed):
    if button == m.Button.left:
        print(f"{button} - {'pressed' if pressed else 'released'}")

kb_listen = kb.Listener(on_press = key_press)
m_listen = m.Listener(on_click = left_click)
kb_listen.start()
m_listen.start()
kb_listen.join()
m_listen.join()