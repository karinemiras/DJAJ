from song import Song
from golive import *
import random

# one random
demos_styles = [random.choice(Song('').presets)]
# all
# demos_styles = Improvisation('').presets

for s in demos_styles:

    song = Song('')
    song.initialize_song()
    song.build_midi()
    song.preset = s
    song.export_midi('current_song_all')
    went_live = False

    while not went_live:
        went_live = go_live_ableton(song)

