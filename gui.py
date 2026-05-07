from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QCheckBox, QWidget
from PyQt5.QtGui import QFont, QCursor, QIcon
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
main_x, main_y = 300, 200
last_x, last_y = 0, 0
kb_controller = kb.Controller()
settings_opened = False
 

def key_press(key):
    global thing, caps, repositions, settings_opened

    if settings_opened or fv.typing:
        return
    
    if key == Key.enter:
        fv.update_word('ent')
        toggle_window(False)
        return

    if key == Key.space:
        fv.update_word(' ')
        repositions = 0
        if thing.settings.auto.isChecked():
             thing.insert_word(True)
        toggle_window(False)
    elif key == Key.backspace:
        fv.update_word('del')
        if len(fv.main_word) < 1:
            toggle_window(False)
        else:
            toggle_window(True)
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
            if len(fv.main_word) == 0 or fv.valid_word == False:
                toggle_window(False)  
                 
def left_click(x, y, button, pressed):
    global thing, repositions, main_x, main_y, settings_opened

    if thing.settings.dont_move.isChecked() or settings_opened or fv.typing:
        return

    if button == m.Button.left:  
        if pressed:
            temp = thing.mapFromGlobal(QCursor.pos())
            if (temp.x() < 0 or temp.x() > thing.frameGeometry().width()) or (temp.y() < 0 or temp.y() > thing.frameGeometry().height()):
                thing.move(x+10, y+50)
                toggle_window(True)

def toggle_window(active):
    global thing

    if not thing.settings.stay.isChecked(): 
        if active:
            thing.show()
        else:
            thing.hide()


class Main_Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.buttons = [QPushButton('-', self) for _ in range(fv.max_predict)]
        
        self.settings = Settings()
        self.settings_button = QPushButton(self)

        self.initUI()

    def update_suggestions(self):
        max_button_width = 0
        fv.update_candidates()
        for i in range(fv.max_predict):
            self.buttons[i].setText(fv.match_caps(fv.suggestions[i]))
            self.buttons[i].adjustSize()
            temp_w = self.buttons[i].frameGeometry().width()
            if temp_w > max_button_width:
                max_button_width = temp_w
        self.setFixedWidth(max_button_width)  

    def insert_word(self, is_auto = False):
        global kb_controller
        
        fv.typing = True
        toggle_window(False)
        fv.suggestions = ['-' for _ in range(fv.max_predict)]
        for _ in range(len(fv.main_word)):
            kb_controller.press(Key.backspace)
            kb_controller.release(Key.backspace)
        if is_auto:
            kb_controller.type(thing.buttons[0].text())
            kb_controller.type(' ')
            fv.full_txt = fv.full_txt[:fv.full_txt.rfind(' ')+1]+thing.buttons[0].text()+' '
        else:
            kb_controller.type(self.sender().text())
            kb_controller.type(' ')
            fv.full_txt = fv.full_txt[:fv.full_txt.rfind(' ')+1]+self.sender().text()+' '
        fv.reset_word()
        fv.typing = False

    def open_settings(self):
        global settings_opened

        settings_opened = True
        self.settings.show()    

    def closeEvent(self, event):
        self.settings.close()

    def initUI(self):
        w, h = 100, 33
        for i in range(fv.max_predict):
            self.buttons[i].setFont(QFont('Corbel', 16))
            self.buttons[i].setStyleSheet(f"color: {'#14a7cc' if i%2 == 0 else '#b714cc'};"
                                          f"background-color: {'#a3c3cc' if i%2 == 0 else '#c6a3cc'};"
                                          'font-weight: bold;')
            self.buttons[i].setGeometry(0, i*h, w, h)
            self.buttons[i].adjustSize()
            self.buttons[i].clicked.connect(self.insert_word)
            self.buttons[i].setFocusPolicy(Qt.NoFocus)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_suggestions)
        self.timer.start(1000)

        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setGeometry(0, 165, 80, 30)
        self.settings_button.setFont(QFont('Corbel', 12))
        self.settings_button.setText('Settings')
        self.settings_button.adjustSize()

        self.settings_button.setFocusPolicy(Qt.NoFocus)

        fv.get_word_list()

class Settings(QWidget):
    def __init__(self):
        super().__init__()

        self.stay = QCheckBox(self)
        self.stay.setText('Keep window active')
        self.stay.setFont(QFont('Corbel', 14))
        self.stay.setGeometry(10, 0, 180, 25)

        self.auto = QCheckBox(self)
        self.auto.setText('Auto-Insert')
        self.auto.setFont(QFont('Corbel', 14))
        self.auto.setGeometry(10, 25, 110, 25)

        self.dont_move = QCheckBox(self)
        self.dont_move.setText('Don\'t Move')
        self.dont_move.setFont(QFont('Corbel', 14))
        self.dont_move.setGeometry(10, 50, 110, 25)
        
        self.initUI()
        
    def closeEvent(self, event):
        global settings_opened

        settings_opened = False

    def initUI(self):
        self.stay.setFocusPolicy(Qt.NoFocus)
        self.auto.setFocusPolicy(Qt.NoFocus)
        self.dont_move.setFocusPolicy(Qt.NoFocus)
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('Settings')

if __name__ == '__main__':
    kb_listen = kb.Listener(on_press = key_press) 
    m_listen = m.Listener(on_click = left_click)
    kb_listen.start()
    m_listen.start()

    app = QApplication(sys.argv)
    
    thing = Main_Menu()
    thing.setWindowIcon(QIcon('icon.png'))
    thing.setGeometry(500, 500, main_x, main_y)
    thing.setFixedSize(main_x, main_y)
    thing.setWindowTitle('Autocorect')
    thing.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    thing.setAttribute(Qt.WA_TranslucentBackground, on = True)
    thing.show()
    thing.setFocusPolicy(Qt.NoFocus)
    
    sys.exit(app.exec_())