from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui, QtCore

class AppInfo(QWidget):

    def __init__(self,
                 _timeout,
                 _times,
                 _beat,
                 _tempo,
                 _key,
                 _karaoke_bars,
                 _pitch_labels,
                 _scale_mode):

        super().__init__()
        super().setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        oImage = QImage("img/b7.png")
        sImage = oImage.scaled(QSize(1670, 930))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        self.title = 'AJ - The Artificial Jammer'
        self.score = 0
        self.left = 5
        self.top = 5
        self.width = 1670
        self.height = 930
        self.timeout = _timeout
        self.times = _times
        self.beat = _beat
        self.tempo = _tempo
        self.key = _key
        self.karaoke_bars = _karaoke_bars
        self.pitch_labels = _pitch_labels
        self.scale_mode = _scale_mode
        self.loading = ''
        self.chords = []

        return self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        labelA = QtWidgets.QLabel(self)
        labelA.setText('Key')
        labelA.setFont(QtGui.QFont("Chalkduster", 20, QtGui.QFont.Bold))
        labelA.setStyleSheet("QLabel {color: #ffffff}")
        labelA.move(160, 875)

        labelB = QtWidgets.QLabel(self)
        labelB.setText(str(self.pitch_labels[self.key]) + ' ' + self.scale_mode)
        labelB.setFont(QtGui.QFont("Chalkduster", 30, QtGui.QFont.Bold))
        labelB.setStyleSheet("QLabel {color: #444444}")
       # labelB.resize(30,30)
        labelB.move(210, 870)

        labelC = QtWidgets.QLabel(self)
        labelC.setText('Time ')
        labelC.setFont(QtGui.QFont("Chalkduster", 20, QtGui.QFont.Bold))
        labelC.setStyleSheet("QLabel {color: #ffffff}")
        labelC.move(550, 875)

        labelD = QtWidgets.QLabel(self)
        labelD.setText(str(self.times) + 'x4')
        labelD.setFont(QtGui.QFont("Chalkduster", 30, QtGui.QFont.Bold))
        labelD.setStyleSheet("QLabel {color: #444444}")
        labelD.move(610, 870)

        labelE = QtWidgets.QLabel(self)
        labelE.setText('Tempo ')
        labelE.setFont(QtGui.QFont("Chalkduster", 20, QtGui.QFont.Bold))
        labelE.setStyleSheet("QLabel {color: #ffffff}")
        labelE.move(950, 875)

        labelF = QtWidgets.QLabel(self)
        labelF.setText(str(self.tempo) + 'bpm')
        labelF.setFont(QtGui.QFont("Chalkduster", 30, QtGui.QFont.Bold))
        labelF.setStyleSheet("QLabel {color: #444444}")
        labelF.move(1030, 870)

        labelG = QtWidgets.QLabel(self)
        labelG.setText('Bar')
        labelG.setFont(QtGui.QFont("Chalkduster", 20, QtGui.QFont.Bold))
        labelG.setStyleSheet("QLabel {color: #ffffff}")
        labelG.move(1340, 875)

        self.bars = QtWidgets.QLabel(self)
        self.bars.setText('----/----')
        self.bars.setFont(QtGui.QFont("Chalkduster", 30, QtGui.QFont.Bold))
        self.bars.setStyleSheet("QLabel {color: #aa0000}")
        self.bars.move(1400, 870)

        self.roles = QLabel(self)
        self.pixmap1 = QPixmap('img/avatar.png')
        self.roles.setPixmap(self.pixmap1)
        self.roles.move(400, 180)

        self.wait = QtWidgets.QLabel(self)
        self.wait.setText('  First, let me think...          ')
        self.wait.setStyleSheet("QLabel {color: #FF93EE}")
        self.wait.setFont(QtGui.QFont("Chalkduster", 30, QtGui.QFont.Bold))
        self.wait.move(660, 610)

        self.wait2 = QtWidgets.QLabel(self)
        self.wait2.setText('        Hmm...          ')
        self.wait2.setStyleSheet("QLabel {color: #FF93EE}")
        self.wait2.setFont(QtGui.QFont("Chalkduster", 25, QtGui.QFont.Bold))
        self.wait2.move(800, 240)

        self.roles = QLabel(self)
        self.pixmap1 = QPixmap('img/sign1.png')
        self.roles.setPixmap(self.pixmap1)
        self.roles.move(50, 130)

        self.roles = QLabel(self)
        self.pixmap1 = QPixmap('img/sign2.png')
        self.roles.setPixmap(self.pixmap1)
        self.roles.move(1300, 130)

        button_exit = QPushButton('', self)
        button_exit.setStyleSheet("background-color: #dddddd;")
        button_exit.move(1645, 900)
        button_exit.resize(10, 10)
        button_exit.clicked.connect(self.quit_aj)

        num_chords = self.karaoke_bars
        ini_x = 50
        ini_y = 30

        for c in range(0, num_chords):
            self.chords.append(QtWidgets.QLabel(self))
            self.chords[-1].setText('          ')
            self.chords[-1].setFont(QtGui.QFont("Chalkduster", 40, QtGui.QFont.Bold))
            self.chords[c].setStyleSheet("QLabel {background-color: #ffffff; color: #ffffff; border: 2px solid #cccccc;}")
            self.chords[-1].resize(130, 70)
            self.chords[-1].move(ini_x, ini_y)
            ini_x += 130
            if c == 11:
                ini_x = 50
                ini_y = 100

        self.show()


    @pyqtSlot()
    def quit_aj(self):
        sys.exit()