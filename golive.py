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
                                 song.key,
                                 song.pitch_labels,
                                 song.scale_mode)

        os.system('all_params='
                  + str(song.preset)
                  + ' osascript as_open.scpt')

        time.sleep(1.5)

        set = live.Set()
        set.scan(scan_devices=True)
        set.tempo = song.tempo

        ap, app = update_loading_label(ap, app)

        # play all tracks
        for t in set.tracks:
            t.clips[0].play()

        # wait for song to finish playing: complete or 2 seconds only
        if not short:
            bar_karaoke = 0
            chords_sequence = 0

            for bar in range(0+1, song.num_bars+1):

                ap, app, delay_of_timer = update_chords_label(ap, app, bar,
                                                              song.num_bars,
                                                              song.karaoke_chords[chords_sequence],
                                                              bar_karaoke)
                time.sleep((song.get_song_duration() / song.num_bars)-delay_of_timer)
                bar_karaoke += 1
                if bar_karaoke == 9:
                    chords_sequence += 1
                    bar_karaoke = 0
        else:
            time.sleep(2)

        # stop all tracks
        os.system('osascript as_focus.scpt')
        for t in set.tracks:
            t.clips[0].stop()

        # saves project and closes ableton
        os.system('osascript as_close.scpt')
        time.sleep(0.5)

        return True

    except:
        return False

