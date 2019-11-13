from interface import *
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
    print('You have:', timeout-count, ' seconds to choose...')
    if count >= timeout:
        QtCore.QCoreApplication.quit()


def get_user_input(max_score, timeout):

    app = QApplication(sys.argv)
    ap = App()
    start_timer(timer_func, timeout)
    app.exec_()

    if ap.score > 0:
        score = ap.score
    else:
        score = random.choice(range(1, max_score + 1))
        print("\nSorry, your time expired or your choice was invalid. A random choice was made for you.\n")

    return score


