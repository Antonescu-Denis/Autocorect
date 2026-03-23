from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QTimer
import funcvar as fv
import sys


class Main_Menu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.buttons = [QPushButton(f"thing {f"{i}"*i}", self) for i in range(fv.max_predict)]

        self.initUI()

    def update_suggestions(self):
        for i in range(fv.max_predict):
            self.buttons[i].setText(fv.word)
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
        self.timer.start(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    thing = Main_Menu()
    thing.setGeometry(0, 0, 500, 500)
    thing.setWindowTitle('Arcaea B30 Calculator :3')
    thing.show()

    sys.exit(app.exec_())