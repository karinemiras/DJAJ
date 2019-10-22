from improvisation import Improvisation
from golive import *

demos_styles = range(1, max(Improvisation.presets)+1)

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

