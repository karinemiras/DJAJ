from improvisation import Improvisation
import live
import os
import time

def go_live_ableton(song):

    os.system('all_params='
              + str(song.instruments)
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
    time.sleep(1)


for i in range(1, 43):

    song_name = 'song_'+str(i)
    song = Improvisation(song_name)
    song.initialize_song()
    song.export_midi(song_name)
    song.export_midi('current_song_all')

    go_live_ableton(song)

