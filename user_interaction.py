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
    print(timeout-count, ' seconds left...')
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
                   pitch_labels,
                   scale_mode
                   ):

    app = QApplication(sys.argv)
    ap = AppInfo(timeout,
                 times,
                 beat,
                 tempo,
                 key,
                 pitch_labels,
                 scale_mode)
    # weird that this works: the timer is being used to proceed to the song playing,
    # and window is closed after it plays. maybe coz this method is called from a trycatch?
    start_timer(timer_func, timeout)
    app.exec_()

    return ap, app


def update_loading_label(ap, app):
    ap.loading.setText('Playing...')
    start_timer(timer_func, 0)
    app.exec()

    return ap, app


def update_chords_label(ap, app, bar, bars, chords, bar_karaoke):

    ap.loading.setText('Playing '+str(bar)+'/'+str(bars))

    for c in range(0, len(ap.chords)):
        ap.chords[c].setText(chords[c]+' ')

        if c == bar_karaoke:
            ap.chords[c].setStyleSheet("QLabel {color: #ffffff}")
        else:
            ap.chords[c].setStyleSheet("QLabel {color: #ff0000}")

    start_timer(timer_func, 0)
    app.exec()
    delay_of_timer = 1

    return ap, app, delay_of_timer


