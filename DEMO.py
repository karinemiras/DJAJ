from song import Song
from golive import *
import argparse
import random

parser = argparse.ArgumentParser()

# choose 'all' or 'random'
parser.add_argument('--type', default='random', help='type of demo to play')
parser.add_argument('--show_visuals', default=False, help='show the ajs graphicals')
parser.add_argument('--load_in_ableton', default=True, help='load composition from midi file generated into an ableton preset')
args = parser.parse_args()

# one random preset
if args.type == 'random':
    demos_styles = [random.choice(Song('').presets)]

# all presets
if args.type == 'all':
    demos_styles = Song('').presets

# just choose some
demos_styles = [3]

for s in demos_styles:
    song = Song()
    song.choices()
    song.preset = s
    song.compose()
    song.build_midi()
    song.build_karaoke()
    song.export_midi('current_song_all')
    print(song.tempo)

    if not (args.load_in_ableton is False and args.show_visuals is False):
        went_live = False
        while not went_live:
            went_live = go_live_ableton(song=song,
                                        load_in_ableton=args.load_in_ableton,
                                        show_visuals=args.show_visuals)

