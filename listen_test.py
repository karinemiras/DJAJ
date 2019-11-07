from golive import *
import argparse
import pickle

parser = argparse.ArgumentParser()

parser.add_argument('--experiment_name', default='default_experiment', help='name of the experiment')
parser.add_argument('--individual', default='1', help='individual id')
args = parser.parse_args()

# allow whole generation later...

with open('experiments/'+args.experiment_name + '/genotypes/individual_'  + str(args.individual) + '.pkl', 'rb') as input:
    song = pickle.load(input)
    song = song[0]
    song.build_midi()
    song.export_midi('current_song_all')
    went_live = False
    while not went_live:
        went_live = go_live_ableton(song)

