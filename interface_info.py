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

        arrow1_1 = QLabel(self)
        pixmap = QPixmap('img/key.png')
        pixmap = pixmap.scaledToWidth(70)
        arrow1_1.setPixmap(pixmap)
        arrow1_1.move(70, 10)

        labelA = QtWidgets.QLabel(self)
        labelA.setText('Key')
        labelA.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelA.setStyleSheet("QLabel {color: #ffffff}")
        labelA.move(90, 135)

        labelB = QtWidgets.QLabel(self)
        labelB.setText(str(self.pitch_labels[self.key]) + ' ' + self.scale_mode)
        labelB.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelB.setStyleSheet("QLabel {color: #FF9933}")
        labelB.move(167, 30)

        labelC = QtWidgets.QLabel(self)
        labelC.setText('Time ')
        labelC.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelC.setStyleSheet("QLabel {color: #ffffff}")
        labelC.move(655, 129)

        labelD = QtWidgets.QLabel(self)
        labelD.setText(str(self.times) + 'x4')
        labelD.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelD.setStyleSheet("QLabel {color: #FF9933}")
        labelD.move(610, 30)

        arrow1_1 = QLabel(self)
        pixmap = QPixmap('img/metro.png')
        pixmap = pixmap.scaledToWidth(90)
        arrow1_1.setPixmap(pixmap)
        arrow1_1.move(860, 20)

        labelE = QtWidgets.QLabel(self)
        labelE.setText('Tempo ')
        labelE.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelE.setStyleSheet("QLabel {color: #ffffff}")
        labelE.move(880, 129)

        labelF = QtWidgets.QLabel(self)
        labelF.setText(str(self.tempo) + 'bpm')
        labelF.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        labelF.setStyleSheet("QLabel {color: #FF9933}")
        labelF.move(990, 30)

        labelG = QtWidgets.QLabel(self)
        labelG.setText('Bar')
        labelG.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        labelG.setStyleSheet("QLabel {color: #ffffff}")
        labelG.move(1455, 129)

        self.bars = QtWidgets.QLabel(self)
        self.bars.setText('----/----')
        self.bars.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
        self.bars.setStyleSheet("QLabel {color: #FF9933}")
        self.bars.move(1370, 30)

        # self.loading = QMovie("img/loading.gif")
        # self.loading.frameChanged.connect(self.repaint)
        # self.loading.setScaledSize(QtCore.QSize(70, 70))
        # self.loading.start()

        self.wait = QtWidgets.QLabel(self)
        self.wait.setText('...wait...')
        self.wait.setFont(QtGui.QFont("Arial", 50, QtGui.QFont.Bold))
        self.wait.setStyleSheet("QLabel {color: #ffffff}")
        self.wait.move(700, 340)

        aj_role = QtWidgets.QLabel(self)
        aj_role.setText("Bars for AJ's solo: in red")
        aj_role.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        aj_role.setStyleSheet("QLabel {color: #aa0000}")
        aj_role.move(430, 480)

        self.roles_aj = QLabel(self)
        pixmap = QPixmap('img/aj_icon.png')
        self.roles_aj.setPixmap(pixmap)
        self.roles_aj.move(460, 320)

        user_role = QtWidgets.QLabel(self)
        user_role.setText('Bars for HUMAN solo: in green')
        user_role.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        user_role.setStyleSheet("QLabel {color: #00aa00}")
        user_role.move(890, 480)

        self.roles_user = QLabel(self)
        pixmap = QPixmap('img/user_icon.png')
        self.roles_user.setPixmap(pixmap)
        self.roles_user.move(940, 330)

        button_exit = QPushButton('', self)
        button_exit.setStyleSheet("background-color: rgb(40,40,40);");
        button_exit.move(1645, 5)
        button_exit.resize(10, 10)
        button_exit.clicked.connect(self.quit_aj)

        num_chords = 10
        ini_x = 150
        ini_y = 200

        for c in range(0, num_chords):
            self.chords.append(QtWidgets.QLabel(self))
            self.chords[-1].setText('        ')
            self.chords[-1].setFont(QtGui.QFont("Arial", 50, QtGui.QFont.Bold))
            self.chords[-1].move(ini_x, ini_y)
            ini_x += 130

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