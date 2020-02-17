import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush

class AppScore(QWidget):

    def __init__(self):
        super().__init__()
        super().setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.title = 'Click on the faces to evaluate the music'
        self.score = 0
        self.left = 5
        self.top = 5
        self.width = 1670
        self.height = 930
        return self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        oImage = QImage("img/b7.png")
        sImage = oImage.scaled(QSize(1670, 930))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.roles = QLabel(self)
        self.pixmap1 = QPixmap('img/avatar.png')
        self.roles.setPixmap(self.pixmap1)
        self.roles.move(100, 20)

        self.wait = QtWidgets.QLabel(self)
        self.wait.setText('  Did you like our music?     ')
        self.wait.setStyleSheet("QLabel {color: #FF93EE}")
        self.wait.setFont(QtGui.QFont("Chalkduster", 30, QtGui.QFont.Bold))
        self.wait.move(320, 450)

        self.wait2 = QtWidgets.QLabel(self)
        self.wait2.setText('        So...      ')
        self.wait2.setStyleSheet("QLabel {color: #FF93EE}")
        self.wait2.setFont(QtGui.QFont("Chalkduster", 25, QtGui.QFont.Bold))
        self.wait2.move(520, 80)

        button1 = QPushButton('', self)
        button1.setStyleSheet('border-image: url(img/f1.png);')
        button1.setGeometry(90, 100, 100, 61)
        button1.move(460, 600)
        button1.resize(190, 190)
        button1.clicked.connect(self.on_click_button1)

        button2 = QPushButton('', self)
        button2.setStyleSheet('border-image: url({})'.format('img/f2.png'))
        button2.setGeometry(100, 100, 100, 61)
        button2.move(660, 595)
        button2.resize(210, 210)
        button2.clicked.connect(self.on_click_button2)

        button3 = QPushButton('', self)
        button3.setStyleSheet('border-image: url({})'.format('img/f3.png'))
        button3.setGeometry(100, 100, 100, 61)
        button3.move(880, 595)
        button3.resize(200, 200)
        button3.clicked.connect(self.on_click_button3)

        button4 = QPushButton('', self)
        button4.setStyleSheet('border-image: url({})'.format('img/f4.png'))
        button4.setGeometry(100, 100, 100, 61)
        button4.move(1100, 595)
        button4.resize(200, 200)
        button4.clicked.connect(self.on_click_button4)

        button5 = QPushButton('', self)
        button5.setStyleSheet('border-image: url({})'.format('img/f5.png'))
        button5.setGeometry(100, 100, 100, 61)
        button5.move(1310, 587)
        button5.resize(208, 232)
        button5.clicked.connect(self.on_click_button5)

        button_exit = QPushButton('', self)
        button_exit.setStyleSheet("background-color: rgb(200,200,200);")
        button_exit.move(1660, 900)
        button_exit.resize(5, 5)
        button_exit.clicked.connect(self.quit_aj)

        self.show()

    @pyqtSlot()
    def on_click_button1(self):
        self.score = 1
        self.close()

    @pyqtSlot()
    def on_click_button2(self):
        self.score = 2
        self.close()

    @pyqtSlot()
    def on_click_button3(self):
        self.score = 3
        self.close()

    @pyqtSlot()
    def on_click_button4(self):
        self.score = 4
        self.close()

    @pyqtSlot()
    def on_click_button5(self):
        self.score = 5
        self.close()

    @pyqtSlot()
    def quit_aj(self):
        sys.exit()


