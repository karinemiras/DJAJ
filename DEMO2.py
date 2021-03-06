from song import Song
from golive import *


# example 1
song = Song()
song.choices()
song.preset = 12
song.key = 36
song.tempo = 135
song.scale_mode = 'major'
song.scale_type = 'pentatonic'
song.times = 4
song.num_bars = 24
song.progression_type = 'blues'
song.compose()
song.build_midi()
song.build_karaoke()
song.export_midi('current_song_all')
went_live = False
while not went_live:
    went_live = go_live_ableton(song)


# example 2
song = Song()
song.choices()
song.preset = 25
song.key = 40
song.tempo = 120
song.scale_mode = 'minor'
song.scale_type = 'pentatonic'
song.times = 4
song.num_bars = 24
song.progression_type = 'fall'
song.compose()
song.build_midi()
song.build_karaoke()
song.export_midi('current_song_all')
went_live = False
while not went_live:
    went_live = go_live_ableton(song)


