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
#demos_styles = [1]

for s in demos_styles:
    song = Song()
    song.num_bars = 12
    song.initialize_song()
    song.build_midi()
    song.build_karaoke()
    song.preset = s
    song.export_midi('current_song_all')

    went_live = False
    while not went_live:
        went_live = go_live_ableton(song, args.short)

