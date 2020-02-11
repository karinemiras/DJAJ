import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSlot, QByteArray
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie, QPainter, QPixmap

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
        self.title = 'Info about the current jam'
        self.score = 0
        self.left = 5
        self.top = 510
        self.width = 1670
        self.height = 530
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

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # self.loading = QMovie("img/loading.gif")
        # self.loading.frameChanged.connect(self.repaint)
        # self.loading.setScaledSize(QtCore.QSize(70, 70))
        # self.loading.start()

        title = QtWidgets.QLabel(self)
        title.setText('You solo in the green bars:')
        title.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        title.setStyleSheet("QLabel {color: #00aa00}")
        title.move(10, 10)

        arrow1_1 = QLabel(self)
        pixmap = QPixmap('img/key.png')
        pixmap = pixmap.scaledToWidth(30)
        arrow1_1.setPixmap(pixmap)
        arrow1_1.move(120, 460)

        labelA = QtWidgets.QLabel(self)
        labelA.setText('Key')
        labelA.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelA.setStyleSheet("QLabel {color: #ffffff}")
        labelA.move(160, 490)

        labelB = QtWidgets.QLabel(self)
        labelB.setText(str(self.pitch_labels[self.key]) + ' ' + self.scale_mode)
        labelB.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        labelB.setStyleSheet("QLabel {color: #FF9933}")
        labelB.move(210, 480)

        labelC = QtWidgets.QLabel(self)
        labelC.setText('Time ')
        labelC.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelC.setStyleSheet("QLabel {color: #ffffff}")
        labelC.move(550, 490)

        labelD = QtWidgets.QLabel(self)
        labelD.setText(str(self.times) + 'x4')
        labelD.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        labelD.setStyleSheet("QLabel {color: #FF9933}")
        labelD.move(610, 480)

        arrow1_1 = QLabel(self)
        pixmap = QPixmap('img/metro.png')
        pixmap = pixmap.scaledToWidth(30)
        arrow1_1.setPixmap(pixmap)
        arrow1_1.move(910, 480)

        labelE = QtWidgets.QLabel(self)
        labelE.setText('Tempo ')
        labelE.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelE.setStyleSheet("QLabel {color: #ffffff}")
        labelE.move(950, 490)

        labelF = QtWidgets.QLabel(self)
        labelF.setText(str(self.tempo) + 'bpm')
        labelF.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        labelF.setStyleSheet("QLabel {color: #FF9933}")
        labelF.move(1030, 480)

        labelG = QtWidgets.QLabel(self)
        labelG.setText('Bar')
        labelG.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelG.setStyleSheet("QLabel {color: #ffffff}")
        labelG.move(1340, 490)

        self.bars = QtWidgets.QLabel(self)
        self.bars.setText('----/----')
        self.bars.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
        self.bars.setStyleSheet("QLabel {color: #aa0000}")
        self.bars.move(1400, 480)

        # self.loading = QMovie("img/loading.gif")
        # self.loading.frameChanged.connect(self.repaint)
        # self.loading.setScaledSize(QtCore.QSize(70, 70))
        # self.loading.start()

        self.wait = QtWidgets.QLabel(self)
        self.wait.setText('...thinking...           ')
        self.wait.setStyleSheet("QLabel {color: #aa0000}")
        self.wait.setFont(QtGui.QFont("Arial", 100, QtGui.QFont.Bold))
        self.wait.move(500, 200)

        self.roles = QLabel(self)
        self.pixmap1 = QPixmap('img/aj_icon.png')
        self.roles.setGeometry(QtCore.QRect(700, 280, 200, 200))
        self.roles.setPixmap(self.pixmap1)

        self.pixmap2 = QPixmap('img/user_icon.png')

        button_exit = QPushButton('', self)
        button_exit.setStyleSheet("background-color: rgb(30,30,30);")
        button_exit.move(1645, 5)
        button_exit.resize(10, 10)
        button_exit.clicked.connect(self.quit_aj)

        num_chords = self.karaoke_bars
        ini_x = 50
        ini_y = 60

        for c in range(0, num_chords):
            self.chords.append(QtWidgets.QLabel(self))
            self.chords[-1].setText('          ')
            self.chords[-1].setFont(QtGui.QFont("Arial", 40, QtGui.QFont.Bold))
            self.chords[c].setStyleSheet("QLabel {color: #aa0000; border: 2px solid #555555;}")
            self.chords[-1].resize(130, 70)
            self.chords[-1].move(ini_x, ini_y)
            ini_x += 130
            if c == 11:
                ini_x = 50
                ini_y = 130

        self.show()

    # def paintEvent(self, event):
    #
    #     ref_x = 750
    #     ref_y = 340
    #     currentFrame = self.loading.currentPixmap()
    #     frameRect = currentFrame.rect()
    #     frameRect.moveCenter(self.rect().center())
    #     if frameRect.intersects(event.rect()):
    #         painter = QPainter(self)
    #         painter.drawPixmap(ref_x, ref_y, currentFrame)

    @pyqtSlot()
    def quit_aj(self):
        sys.exit()