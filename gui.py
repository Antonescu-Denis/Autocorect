from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QCheckBox
from PyQt5.QtGui import QFont, QCursor
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
main_x, main_y = 400, 300
last_x, last_y = 0, 0
 

def key_press(key):
    global thing, caps, repositions
    
    if key == Key.enter:
        thing.temp_stop.setChecked(False)
        fv.update_word('ent')
        toggle_window(False)
        return
    elif thing.temp_stop.isChecked():
        return

    if key == Key.space:
        fv.update_word(' ')
        toggle_window(False)
        repositions = 0
        if thing.auto.isChecked():
             thing.insert_word(True)
    elif key == Key.backspace:
        fv.update_word('del')
    elif key == Key.caps_lock:
        caps = not caps
    elif key == Key.shift_l or key == Key.shift_r:
        pass
    else:
        try:
            k = key.char
            if k:
                fv.update_word(k.upper() if caps else k)
                if fv.valid_word and k.isalpha() and k.isascii():
                    toggle_window(True)
                else:
                    toggle_window(False)
        except Exception:
            if len(fv.word) == 0 or fv.valid_word == False:
                toggle_window(False)  
                 
def left_click(x, y, button, pressed): 
    global thing, repositions, main_x, main_y

    if button == m.Button.left:  
        if pressed and repositions < 5:
            temp = thing.mapFromGlobal(QCursor.pos())
            if (temp.x() < 0 or temp.x() > main_x) or (temp.y() < -30 or temp.y() > main_y):
                thing.move(x+10, y+50)
                toggle_window(True)
                repositions += 1

def toggle_window(active): 
    global thing
    
    if thing.temp_stop.isChecked():
        return

    if not thing.stay.isChecked(): 
        if active:
            thing.showNormal()
        else:
            thing.showMinimized()

class Main_Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.buttons = [QPushButton(f"thing {f"{i}"*i}", self) for i in range(fv.max_predict)]

        self.stay = QCheckBox(self)
        self.stay.setText('Keep window active')
        self.stay.setFont(QFont('Corbel', 14))
        self.stay.setGeometry(10, 250, 180, 25)
        self.stay.setStyleSheet('background-color: #ffffff')

        self.auto = QCheckBox(self)
        self.auto.setText('Auto-Insert')
        self.auto.setFont(QFont('Corbel', 14))
        self.auto.setGeometry(10, 275, 110, 25)
        self.auto.setStyleSheet('background-color: #ffffff')

        self.temp_stop = QCheckBox(self)
        self.temp_stop.setText('Temporarily stop')
        self.temp_stop.setFont(QFont('Corbel', 14))
        self.temp_stop.setGeometry(125, 275, 150, 25)
        self.temp_stop.setStyleSheet('background-color: #ffffff')

        self.initUI()

    def update_suggestions(self):
        for i in range(fv.max_predict):
            self.buttons[i].setText(f"{i+1}: {fv.suggestions[i]}")
            self.buttons[i].adjustSize()

    def insert_word(self, is_auto = False):
        toggle_window(False)
        fv.full_txt += ' '
        fv.word = ''
        fv.suggestions = [fv.word for _ in range(fv.max_predict)]
        if is_auto:
            print(f"auto-{thing.buttons[0].text()}")
        else:
            print(self.sender().text())

    def temp_hide(self):
        self.showMinimized()

    def initUI(self):
        w, h = 200, 50
        for i in range(fv.max_predict):
            self.buttons[i].setFont(QFont('Corbel', 20))
            self.buttons[i].setStyleSheet(f"color: {'#14a7cc' if i%2 == 0 else '#b714cc'};"
                                          f"background-color: {'#a3c3cc' if i%2 == 0 else '#c6a3cc'};"
                                          'font-weight: bold;')
            self.buttons[i].setGeometry(0, i*h, w, h)
            self.buttons[i].adjustSize()
            self.buttons[i].clicked.connect(self.insert_word)
            self.buttons[i].setFocusPolicy(Qt.NoFocus)

        self.temp_stop.clicked.connect(self.temp_hide)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_suggestions)
        self.timer.start(100)

        self.stay.setFocusPolicy(Qt.NoFocus)
        self.auto.setFocusPolicy(Qt.NoFocus)


if __name__ == '__main__':
    kb_listen = kb.Listener(on_press = key_press) 
    m_listen = m.Listener(on_click = left_click)
    kb_listen.start()
    m_listen.start()

    app = QApplication(sys.argv)
    
    thing = Main_Menu()
    thing.setGeometry(500, 100, main_x, main_y)
    thing.setFixedSize(main_x, main_y)
    thing.setWindowTitle('Arcaea B30 Calculator :3')
    thing.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
    thing.show()    
    
    sys.exit(app.exec_())