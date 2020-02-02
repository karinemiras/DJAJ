import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt


class AppScore(QWidget):

    def __init__(self):
        super().__init__()
        super().setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.title = 'Click on the faces to evaluate the previous jam'
        self.score = 0
        self.left = 240
        self.top = 600
        self.width = 1200
        self.height = 350
        return self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        labelA = QtWidgets.QLabel(self)
        labelA.setText('How did you like this jam?')
        labelA.setFont(QtGui.QFont("Arial", 50, QtGui.QFont.Bold))
        labelA.setStyleSheet("QLabel {color: #FF9933}")
        labelA.move(270, 20)

        button1 = QPushButton('', self)
        button1.setStyleSheet('border-image: url(img/f1.png);')
        button1.setGeometry(90, 100, 100, 61)

        button1.move(60, 120)
        button1.resize(190, 190)
        button1.clicked.connect(self.on_click_button1)

        button2 = QPushButton('', self)
        button2.setStyleSheet('border-image: url({})'.format('img/f2.png'))
        button2.setGeometry(100, 100, 100, 61)
        button2.move(260, 115)
        button2.resize(210, 210)
        button2.clicked.connect(self.on_click_button2)

        button3 = QPushButton('', self)
        button3.setStyleSheet('border-image: url({})'.format('img/f3.png'))
        button3.setGeometry(100, 100, 100, 61)
        button3.move(480, 115)
        button3.resize(200, 200)
        button3.clicked.connect(self.on_click_button3)

        button4 = QPushButton('', self)
        button4.setStyleSheet('border-image: url({})'.format('img/f4.png'))
        button4.setGeometry(100, 100, 100, 61)
        button4.move(700, 115)
        button4.resize(200, 200)
        button4.clicked.connect(self.on_click_button4)

        button5 = QPushButton('', self)
        button5.setStyleSheet('border-image: url({})'.format('img/f5.png'))
        button5.setGeometry(100, 100, 100, 61)
        button5.move(910, 110)
        button5.resize(210, 235)
        button5.clicked.connect(self.on_click_button5)

        button_exit = QPushButton('', self)
        button_exit.setStyleSheet("background-color: rgb(40,40,40);");
        button_exit.move(1180, 10)
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


