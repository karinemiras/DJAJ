import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5 import QtWidgets, QtGui, QtCore


class App(QWidget):

    def __init__(self):
        super().__init__()
        super().setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.title = 'Evaluation of song quality'
        self.score = 0
        self.left = 400
        self.top = 400
        self.width = 740
        self.height = 250
        return self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        labelA = QtWidgets.QLabel(self)
        labelA.setText('Click on a score to evaluate the song you just heard.')
        labelA.setFont(QtGui.QFont("Arial", 25, QtGui.QFont.Bold))
        labelA.move(70, 20)

        button1 = QPushButton('1', self)
        button1.setStyleSheet("background-color:#E50B0B;font:bold;font-size:70px")
        button1.move(50, 70)
        button1.resize(120, 100)
        button1.clicked.connect(self.on_click_button1)

        button2 = QPushButton('2', self)
        button2.setStyleSheet("background-color:#FA6767;font:bold;font-size:70px")
        button2.move(180, 70)
        button2.resize(120, 100)
        button2.clicked.connect(self.on_click_button2)

        button3 = QPushButton('3', self)
        button3.setStyleSheet("background-color:#838383;font:bold;font-size:70px")
        button3.move(310, 70)
        button3.resize(120, 100)
        button3.clicked.connect(self.on_click_button3)

        button4 = QPushButton('4', self)
        button4.setStyleSheet("background-color:#71D488;font:bold;font-size:70px")
        button4.move(440, 70)
        button4.resize(120, 100)
        button4.clicked.connect(self.on_click_button4)

        button5 = QPushButton('5', self)
        button5.setStyleSheet("background-color:#009222;font:bold;font-size:70px")
        button5.move(570, 70)
        button5.resize(120, 100)
        button5.clicked.connect(self.on_click_button5)

        button_exit = QPushButton('', self)
        button_exit.move(10, 230)
        button_exit.resize(20, 10)
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

