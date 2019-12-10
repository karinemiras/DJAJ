from song import Song
from golive import *
import argparse
import random

parser = argparse.ArgumentParser()

# choose 'all' or 'random'
parser.add_argument('--type', default='random', help='type of demo to play')
parser.add_argument('--short', default=False, help='if plays only a small subset of the song')
args = parser.parse_args()

# one random preset
if args.type == 'random':
    demos_styles = [random.choice(Song('').presets)]

# all presets
if args.type == 'all':
    demos_styles = Song('').presets

# just choose some
# demos_styles = _presets = [16, 33, 25, 26, 28,
#             30, 31, 32, 17, 34, 35, 36,
#             37, 38, 41, 43, 44, 45, 47,
#             48, 49]

for s in demos_styles:
    song = Song()
    song.choices()
    song.preset = s
    song.compose()
    song.build_midi()
    song.build_karaoke()
    song.export_midi('current_song_all')

    went_live = False
    while not went_live:
        went_live = go_live_ableton(song, args.short)

