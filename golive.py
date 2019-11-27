from user_interaction import *
import live
import os
import time


def go_live_ableton(song, short=False):

    try:

        ap, app = show_song_info(0,
                                 song.times,
                                 song.beat,
                                 song.tempo,
                                 song.pitch_labels[song.key],
                                 song.scale_mode)

        os.system('all_params='
                  + str(song.preset)
                  + ' osascript as_open.scpt')

        time.sleep(1.5)

        set = live.Set()
        set.scan(scan_devices=True)
        set.tempo = song.tempo

        update_loading_label(ap, app)

        # play all tracks
        for t in set.tracks:
            t.clips[0].play()

        # wait for song to finish playing: complete or 2 seconds
        if not short:
            time.sleep(song.get_song_duration())
        else:
            time.sleep(2)

        # stop all tracks
        for t in set.tracks:
            t.clips[0].stop()

        # saves project and closes ableton
        os.system('osascript as_close.scpt')
        time.sleep(0.5)

        return True

    except:
        return False

