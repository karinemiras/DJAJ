import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot, QByteArray
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt


class AppInfo(QWidget):

    def __init__(self,
                 _timeout,
                 _times,
                 _beat,
                 _tempo,
                 _key,
                 _pitch_labels,
                 _scale_mode):

        super().__init__()
        super().setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.title = 'Info about the current jam'
        self.score = 0
        self.left = 50
        self.top = 70
        self.width = 1580
        self.height = 260
        self.timeout = _timeout
        self.times = _times
        self.beat = _beat
        self.tempo = _tempo
        self.key = _key
        self.pitch_labels = _pitch_labels
        self.scale_mode = _scale_mode
        self.loading = ''
        self.chords = []

        return self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        labelA = QtWidgets.QLabel(self)
        labelA.setText('Key: ')
        labelA.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelA.setStyleSheet("QLabel {color: #ffffff}")
        labelA.move(5, 20)

        labelB = QtWidgets.QLabel(self)
        labelB.setText(str(self.pitch_labels[self.key]) + ' ' + self.scale_mode)
        labelB.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelB.setStyleSheet("QLabel {color: #FF9933}")
        labelB.move(195, 20)

        labelC = QtWidgets.QLabel(self)
        labelC.setText('Time: ')
        labelC.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelC.setStyleSheet("QLabel {color: #ffffff}")
        labelC.move(555, 20)

        labelD = QtWidgets.QLabel(self)
        labelD.setText(str(self.times)+'x4')
        labelD.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelD.setStyleSheet("QLabel {color: #FF9933}")
        labelD.move(785, 20)

        labelE = QtWidgets.QLabel(self)
        labelE.setText('Tempo: ')
        labelE.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelE.setStyleSheet("QLabel {color: #ffffff}")
        labelE.move(960, 20)

        labelF = QtWidgets.QLabel(self)
        labelF.setText(str(self.tempo)+'bpm')
        labelF.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelF.setStyleSheet("QLabel {color: #FF9933}")
        labelF.move(1245, 20)

        self.loading = QtWidgets.QLabel(self)
        self.loading.setText('...Wait...          ')
        self.loading.setFont(QtGui.QFont("Arial", 50, QtGui.QFont.Bold))
        self.loading.setStyleSheet("QLabel {color: #aa0000}")
        self.loading.move(635, 120)

        button_exit = QPushButton('', self)
        button_exit.setStyleSheet("background-color: rgb(40,40,40);");
        button_exit.move(1555, 5)
        button_exit.resize(5, 5)
        button_exit.clicked.connect(self.quit_aj)

        num_chords = 10
        ini_x = 150
        ini_y = 200

        for c in range(0, num_chords):
            self.chords.append(QtWidgets.QLabel(self))
            self.chords[-1].setText('------ ')
            self.chords[-1].setFont(QtGui.QFont("Arial", 50, QtGui.QFont.Bold))
            self.chords[-1].setStyleSheet("QLabel {color: #aa0000}")
            self.chords[-1].move(ini_x, ini_y)
            ini_x += 130

        self.show()

    @pyqtSlot()
    def quit_aj(self):
        sys.exit()

