from interface_score import *
from interface_info import *
import random


def start_timer(slot, timeout=1, interval=1000):
    counter = 0
    def handler():
        nonlocal counter
        counter += 1
        slot(counter, timeout)
        if counter >= timeout:
            timer.stop()
            timer.deleteLater()
    timer = QtCore.QTimer()
    timer.timeout.connect(handler)
    timer.start(interval)


def timer_func(count, timeout):
    #print(timeout-count, ' seconds left...')
    if count >= timeout:
        QtCore.QCoreApplication.quit()


def get_user_input(max_score, timeout):

    app = QApplication(sys.argv)
    ap = AppScore()
    start_timer(timer_func, timeout)
    app.exec_()

    if ap.score > 0:
        score = ap.score
    else:
        score = random.choice(range(1, max_score + 1))
        print("\nSorry, your time expired or your choice was invalid. A random choice was made for you.\n")

    return score


def show_song_info(timeout,
                   times,
                   beat,
                   tempo,
                   key,
                   karaoke_bars,
                   pitch_labels,
                   scale_mode
                   ):

    app = QApplication(sys.argv)
    ap = AppInfo(timeout,
                 times,
                 beat,
                 tempo,
                 key,
                 karaoke_bars,
                 pitch_labels,
                 scale_mode)
    # weird that this works: the timer is being used to proceed to the song playing,
    # and window is closed after it plays. maybe coz this method is called from a trycatch?
    start_timer(timer_func, timeout)
    app.exec_()

    return ap, app


def update_chords_label(ap, app, bar, bars, chords, bar_karaoke, roles):

    ap.bars.setText(str(bar)+'/'+str(bars))

    for c in range(0, len(ap.chords)):
        ap.chords[c].setText(chords[c]+' ')
        ap.chords[c].setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))

        if roles[c] == 'aj':
             ap.chords[c].setStyleSheet("QLabel {color: #aa0000; border: 2px solid #aa0000;}")

        if roles[c] == 'user':
            ap.chords[c].setStyleSheet("QLabel {color: #00aa00; border: 2px solid #00aa00;}")

        if c == bar_karaoke:
            ap.chords[c].setStyleSheet("QLabel {color: #ffffff; border: 2px solid #ffffff;}")
            ap.chords[c].setFont(QtGui.QFont("Arial", 40, QtGui.QFont.Bold))

            if roles[c] == 'aj':
                ap.wait.setText('                       AJ is soloing...')
                ap.wait.setStyleSheet("QLabel {color: #aa0000}")
                ap.wait.setFont(QtGui.QFont("Arial", 30, QtGui.QFont.Bold))
                ap.roles.setPixmap(ap.pixmap1)

            if roles[c] == 'user':
                ap.wait.setText(' You solo now!')
                ap.wait.setStyleSheet("QLabel {color: #00aa00}")
                ap.wait.setFont(QtGui.QFont("Arial", 80, QtGui.QFont.Bold))
                ap.roles.setPixmap(ap.pixmap2)

    #ap.loading.setScaledSize(QtCore.QSize(1, 1))

    start_timer(timer_func, 0)
    app.exec()
    delay_of_timer = 1

    return ap, app, delay_of_timer
