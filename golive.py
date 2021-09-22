from user_interaction import *
import live
import os
import time
import traceback
import sys

def go_live_ableton(song, load_in_ableton=True, show_visuals=True):

    short = False

    try:

        if show_visuals:
            ap, app = show_song_info(0,
                                     song.times,
                                     song.beat,
                                     song.tempo,
                                     song.key,
                                     song.karaoke_bars,
                                     song.pitch_labels,
                                     song.scale_mode)

        if load_in_ableton:
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

        # wait for song to finish playing: complete or 5 seconds only
        if not short:
            bar_karaoke = 0
            chords_sequence = 0

            for bar in range(0+1, song.num_bars+1):
                delay_of_timer = 0
                if show_visuals:
                    ap, app, delay_of_timer = update_chords_label(ap, app, bar,
                                                                  song.num_bars,
                                                                  song.karaoke_chords[chords_sequence],
                                                                  bar_karaoke,
                                                                  song.karaoke_roles[chords_sequence])

                time.sleep((song.get_song_duration() / song.num_bars)-delay_of_timer)
                bar_karaoke += 1

                if bar_karaoke == 12 and chords_sequence < len(song.karaoke_chords)-1:
                    chords_sequence += 1
                    bar_karaoke = 0

        else:

            time.sleep(2)

        if load_in_ableton:
            os.system('osascript as_focus.scpt')

            for t in set.tracks:
                t.clips[0].stop()

        return True

    except Exception as error:
        print('ERROR: {}'.format(traceback.format_exc()))
        sys.exit()
        #time.sleep(1)
