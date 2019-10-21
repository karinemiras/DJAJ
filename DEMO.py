from improvisation import Improvisation
from golive import *

demos_styles = [33, 27, 29, 4, 30, 39, 38]
#demos_styles =  range(1,43)

for s in demos_styles:

    song_name = 'song_'+str(s)
    song = Improvisation(song_name)
    song.initialize_song()
    song.build_midi()
    song.preset = s
    song.export_midi('current_song_all')
    went_live = False

    while not went_live:
        went_live = go_live_ableton(song)

