import live
import os
import time


def go_live_ableton(song):

    try:

        os.system('all_params='
                  + str(song.preset)
                  + ' osascript as_open.scpt')
        time.sleep(1)

        set = live.Set()
        set.scan(scan_devices=True)
        set.tempo = song.tempo

        # play all tracks
        for t in set.tracks:
            t.clips[0].play()

        # wait for song to finish playing
        time.sleep(song.get_song_duration())

        # stop all tracks
        for t in set.tracks:
            t.clips[0].stop()

        # saves project and closes ableton
        os.system('osascript as_close.scpt')
        time.sleep(0.5)

        return True

    except:
        return False

