from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
import funcvar as fv
import sys
from pynput import keyboard as kb
from pynput import mouse as m
from pynput.keyboard import Key


kb_listen = None
m_listen = None
thing = None
caps = False
repositions = 0


def key_press(key):
    global thing, caps, repositions

    if key == Key.space:
        fv.update_word(' ')
        thing.hide()
        repositions = 0
    elif key == Key.backspace:
        fv.update_word('del')
    elif key == Key.enter:
        fv.update_word('ent')
        thing.hide()
    elif key == Key.caps_lock:
        caps = True
    elif key == Key.shift_l or key == Key.shift_r:
        pass
    else:
        try:
            k = key.char
            if k:
                fv.update_word(k.upper() if caps else k)
                if fv.valid_word and k.isalpha() and k.isascii():
                    thing.show()
        except Exception:
            thing.hide()

    if len(fv.word) == 0 or fv.valid_word == False:
        thing.hide()

    print(fv.valid_word)
    print(f"full word: {fv.full_txt}\nword: {fv.word}\n")

def left_click(x, y, button, pressed):
    global thing, repositions

    if button == m.Button.left:
        if pressed and repositions < 3:
            thing.show()
            thing.move(x+10, y+50)
            repositions += 1


class Main_Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.buttons = [QPushButton(f"thing {f"{i}"*i}", self) for i in range(fv.max_predict)]

        self.initUI()

    def update_suggestions(self):
        for i in range(fv.max_predict):
            self.buttons[i].setText(fv.suggestions[i])
            self.buttons[i].adjustSize()

    def initUI(self):
        w, h = 200, 50
        for i in range(fv.max_predict):
            self.buttons[i].setFont(QFont('Corbel', 20))
            self.buttons[i].setStyleSheet(f'color: {'#14a7cc' if i%2 == 0 else '#b714cc'};'
                                          f'background-color: {'#a3c3cc' if i%2 == 0 else '#c6a3cc'};'
                                          'font-weight: bold;')
            self.buttons[i].setGeometry(0, i*h, w, h)
            self.buttons[i].adjustSize()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_suggestions)
        self.timer.start(100)


if __name__ == '__main__':
    kb_listen = kb.Listener(on_press = key_press)
    m_listen = m.Listener(on_click = left_click)
    kb_listen.start()
    m_listen.start()

    app = QApplication(sys.argv)
    
    thing = Main_Menu()
    thing.setGeometry(0, 0, 400, 250)
    thing.setWindowTitle('Arcaea B30 Calculator :3')
    thing.setWindowFlags(Qt.WindowStaysOnTopHint)
    thing.show()    
    
    sys.exit(app.exec_())