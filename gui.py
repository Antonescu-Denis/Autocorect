from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    stacked_widget.setWindowTitle('Arcaea B30 Calculator :3')
    stacked_widget.setGeometry(window_x, window_y, main_w, main_h)
    stacked_widget.setFixedSize(main_w, main_h)
    stacked_widget.setWindowIcon(QIcon(resources+'icon.png'))

    sys.exit(app.exec_())





from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QFont, QPixmap, QPainter
from funcvar import *


class Main_Menu(QWidget):
    def __init__(self):
        super().__init__()

        self.bg_pic = QPixmap(resources+'main bg.jpg')
        
        self.buttons = [QPushButton('B30', self),
                        QPushButton('Profile', self),
                        QPushButton('Guide', self),
                        QPushButton('Scores', self)]

        self.initUI()


    def initUI(self):
        w, h = 190, 70
        x = [0.5, 0.75, 0.5, 0.25]
        y = [0.25, 0.5, 0.75, 0.5]
        colour = ['#14a7cc', '#b714cc', '#b714cc', '#14a7cc']
        bg_colour = ['#c6a3cc', '#c6a3cc', '#a3c3cc', '#a3c3cc']
        for i in range(len(self.buttons)):
            self.buttons[i].setGeometry(pos(x[i], w), pos(y[i], h, 1), w, h)
            self.buttons[i].setFont(QFont('Corbel', 20))
            self.buttons[i].setStyleSheet(f'color: {colour[i]};'
                                          f'background-color: {bg_colour[i]};'
                                          'font-weight: bold;')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg_pic)