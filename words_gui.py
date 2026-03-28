from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import funcvar as fv
import sys
from pynput import keyboard as kb
from pynput import mouse as m
from pynput.keyboard import Key


def key_press(key):
    if key == Key.space:
        fv.update_word(' ')
    elif key == Key.backspace:
        fv.update_word('del')
    elif key == Key.enter:
        fv.update_word('ent')
    else:
        try:
            k = key.char
            if ord(k) < 32:
                fv.ctrl = True
            if k and k.isascii() and k.isalpha():
                fv.update_word(k)
        except Exception:
            pass

def key_release(key):
    try:
        k = key.char
        if ord(k) < 32:
            fv.ctrl = False
    except Exception:
        pass

def left_click(x, y, button, pressed):
    if button == m.Button.left:
        print(f"{button} - {'pressed' if pressed else 'released'}")


class Main_Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.buttons = [QPushButton(f"thing {f"{i}"*i}", self) for i in range(fv.max_predict)]

        self.initUI()

    def update_suggestions(self):
        if fv.ctrl:
            return
        for i in range(fv.max_predict):
            self.buttons[i].setText(fv.suggestions[i])
            self.buttons[i].adjustSize()

    def initUI(self):
        w, h = 200, 50
        colours = ['#14a7cc', '#b714cc']
        bg_colours = ['#a3c3cc', '#c6a3cc']
        for i in range(fv.max_predict):
            self.buttons[i].setFont(QFont('Corbel', 20))
            self.buttons[i].setStyleSheet(f'color: {colours[i%2]};'
                                          f'background-color: {bg_colours[i%2]};'
                                          'font-weight: bold;')
            self.buttons[i].setGeometry(0, i*h, w, h)
            self.buttons[i].adjustSize()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_suggestions)
        self.timer.start(1000)

if __name__ == '__main__':
    kb_listen = kb.Listener(on_press = key_press, on_release = key_release)
    m_listen = m.Listener(on_click = left_click)
    kb_listen.start()
    m_listen.start()

    app = QApplication(sys.argv)
    
    thing = Main_Menu()
    thing.setGeometry(0, 0, 500, 500)
    thing.setWindowTitle('Arcaea B30 Calculator :3')
    thing.show()
    
    sys.exit(app.exec_())