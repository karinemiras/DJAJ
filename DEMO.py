from song import Song
from golive import *
import argparse
import random

parser = argparse.ArgumentParser()

# choose 'all' or 'random'
parser.add_argument('--type', default='one', help='type of demo to play')
args = parser.parse_args()

# one random preset
if args.type == 'random':
    demos_styles = [random.choice(Song('').presets)]

# all presets
if args.type == 'all':
    demos_styles = Song('').presets

for s in demos_styles:

    song = Song('')
    song.initialize_song()
    song.build_midi()
    song.preset = s
    song.export_midi('current_song_all')
    went_live = False
    while not went_live:
        went_live = go_live_ableton(song)

