from pynput.keyboard import Key
import wordfreq, Levenshtein


def on_press(key):
    if key in [Key.esc, Key.space, Key.enter]:
        print()
    else:
        k = ''
        try:
            k = key.char
        except:
            pass
        print(k)

listener = kb.Listener(on_press = on_press)
listener.start()
listener.join()