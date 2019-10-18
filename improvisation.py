"""
Author: Karine Miras - 9/2019
"""

from midi2audio import FluidSynth
from midiutil import MIDIFile

from initialization import Initialization

import numpy as np
import random
import operator
import math
import sys
from datetime import datetime



class Improvisation(Initialization):


    def __init__(self, _song_name):

        # Identification of the track/individual
        self.song_name = _song_name
        # Genotype
        self.genotype = {}
        self.phenotype = None
        # Key of the scale
        self.key = None
        # Scale category
        self.scale_type = None
        # Modality of the key
        self.scale_mode = None
        # All pitchs available within the key
        self.scale_keyboard = None
        # Metronome/speed
        self.tempo = None
        self.times = None
        self.drummed = None
        self.progression = []

        self.duration_pool = {
                            'semibreve': 1*4,
                            'minima': 1*2,
                            'seminima': 1,
                            'colcheia': 1/2,
                            'semicolcheia': 1/4
        }
        self.beat = self.duration_pool['seminima']
        # quaternary is more likely
        self.times_pool = [3] + [4]*5
        # Use multiples of 12
        self.num_bars = 12
        # Tracks info
        self.tracks = {
            'drums' : 3,
            'bass' : 0,
            'chords': 1,
            'solo' : 2
        }
        self.melody_granularities = [3, 4]
        # Channels left and right
        self.num_channels = 2
        # Volumes by track
        self.volumes = {
            'bass' : 130,
            'chords' : 80,
            'solo' : 150,
            'drums' : 110
        }

        # Central C is normally C4 (60) - but in Garage band, it is 72
        # Lowest pool (C1)
        self.low_ref1 = 36
        # Second lowest pool (C2)
        self.low_ref2 = 48
        self.melody_reach = 36

        self.pitch_pool = range(self.low_ref1, self.low_ref1+12, 1)
        self.num_octaves = 5
        self.drummed_prob = 0.9
        self.silent_bars = 0.1
        # Labels for all pitchs of the keyboard, regardless key
        self.pitch_labels = {}

        self.scale_types = ['pentatonic',
                           'pentablues']

        self.scale_modes = [
                          'major',
                          'minor']

        self.intervals_dic = {
                                    'T': 0,
                                    '2m': 1,
                                    '2M': 2,
                                    '3m': 3,
                                    '3M': 4,
                                    '4J': 5,
                                    '4A': 6,
                                    '5J': 7,
                                    '6m': 8,
                                    '6M': 9,
                                    '7m': 10,
                                    '7M': 11,
                                    '8J': 12
                                    }

        # instruments preset
        self.instruments = range(1, 42, 1)

        #  Minimum and maximum speed in BPM.

        self.tempo_pool = {'min': 90, 'mean': 130, 'std': 30, 'max': 190}
        # export 'all' tracks together or 'track' by track
        self.tracks_granularity = 'all'


    def build_pitch_labels(self):

        pitch_labels_basic ={36: 'C',
                             37: 'D#',
                             38: 'D',
                             39: 'Eb',
                             40: 'E',
                             41: 'F',
                             42: 'F#',
                             43: 'G',
                             44: 'Ab',
                             45: 'A',
                             46: 'Bb',
                             47: 'B'}

        self.pitch_labels = pitch_labels_basic.copy()
        self.pitch_labels[0] = 'rest'
        for key, value in pitch_labels_basic.items():
            for oct in range(0, self.num_octaves):
                self.pitch_labels[key+12*oct] = value


    def get_song_duration(self):

        total_beats = self.beat * self.times  * self.num_bars
        minute_portion = total_beats / self.tempo
        seconds = minute_portion * 60
        return seconds

    def build_midi(self):

        if self.tracks_granularity == 'track':

            for track in self.genotype:
                self.phenotype = MIDIFile(
                    numTracks=len(self.tracks),
                    deinterleave=False)
                self.phenotype.addTempo(0,  # track
                                        0,  # time
                                        self.tempo)
                self.add_notes_midi(track)

                self.export_midi(self.song_name+'_'+track)

        else:
            self.phenotype = MIDIFile(
                    numTracks=len(self.tracks),
                    deinterleave=False)
            self.phenotype.addTempo(0,#track
                                    0,#time
                                    self.tempo)
            for track in self.genotype:
                self.add_notes_midi(track)


    def add_notes_midi(self, track):
        for idx_note in range(0, len(self.genotype[track])):
            self.phenotype.addNote(self.genotype[track][idx_note]['track'],
                                   self.genotype[track][idx_note]['channel'],
                                   self.genotype[track][idx_note]['pitch'],
                                   self.genotype[track][idx_note]['time'],
                                   self.genotype[track][idx_note]['duration'],
                                   self.volumes[track])


    def export_metadata(self):
        pass


    def export_midi(self, name):
        with open(name+'.mid', "wb") as output_file:
            self.phenotype.writeFile(output_file)


    def play_midi(self):
        if self.tracks_granularity == 'all':
            fs = FluidSynth()
            fs.play_midi(self.song_name+'.mid')
        else:
            print('MIDIs were exported track by track, thus will not play.')

