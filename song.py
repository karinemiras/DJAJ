"""
Author: Karine Miras - 9/2019
"""

from midi2audio import FluidSynth
from midiutil import MIDIFile

import math
import numpy as np
import random
import pprint

class Song:

    def __init__(self, _song_id='', _num_bars=12, _presets=range(1, 51+1, 1)):

        # Identification of the track/individual
        self.song_id = _song_id
        self.genotype = {}
        self.phenotype = None
        # Key of the scale
        self.key = None
        # Scale category
        self.scale_type = None
        # Modality of the key
        self.scale_mode = None
        # All pitches available within the key
        self.scale_keyboard_full = None
        self.scale_keyboard_filtered = None
        # Metronome/speed
        self.tempo = None
        self.times = None
        self.drummed = None
        self.progression = []
        self.progression_type = None
        self.preset = None
        self.silent_bars = None
        self.karaoke_chords = []

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
        self.num_bars = _num_bars
        # Tracks info
        self.tracks = {
            'percussion': 3,
            'bass': 0,
            'harmony': 1,
            'solo': 2
        }
        self.melody_granularities = [2, 3, 4]
        # Channels left and right
        self.num_channels = 2
        # Volumes by track
        self.volumes = {
            'bass': 130,
            'harmony': 80,
            'solo': 150,
            'percussion': 110
        }

        # Central C is normally C4 (60) - but in Garage band, it is 72
        # Lowest pool (C1)
        self.low_ref1 = 36
        # Second lowest pool (C2)
        self.low_ref2 = 48
        self.melody_reach = 36

        self.pitch_pool = range(self.low_ref1, self.low_ref1+12, 1)
        self.num_octaves = 5
        self.drummed_prob = 1
        # Labels for all pitches of the keyboard, regardless key
        self.pitch_labels = {}

        self.scale_types = ['pentatonic',
                           'pentablues']

        self.scale_modes = [
                          'major',
                          'minor']

        # Free has more chance of happening than fixed progressions.
        self.progression_types = ['blues', 'fall']
        self.progression_types.extend(['free'] * 4)

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
        self.presets = _presets

        #  Minimum and maximum speed in BPM.
        self.tempo_pool = {'min': 90, 'mean': 130, 'std': 20, 'max': 180}

        # export 'all' tracks together or 'track' by track
        self.tracks_granularity = 'all'

    def build_pitch_labels(self):

       # accidents = ['#', 'b']
        pitch_labels_basic ={36: 'C',
                             37: 'Db',
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

    def choices(self):
        self.tempo = int(min(max(np.random.normal(self.tempo_pool['mean'], self.tempo_pool['std'], 1)[0],
                                 self.tempo_pool['min']),
                             self.tempo_pool['max']))
        self.key = random.choice(self.pitch_pool)
        self.silent_bars = random.uniform(0.1, 0.3)
        self.scale_mode = random.choice(self.scale_modes)
        self.scale_type = random.choice(self.scale_types)
        self.times = random.choice(self.times_pool)
        self.preset = random.choice(self.presets)
        self.progression_type = random.choice(self.progression_types)
        self.drummed = True if random.uniform(0, 1) <= self.drummed_prob else False

    def compose(self):

        self.build_pitch_labels()
        self.build_scale()

        self.compose_progression()

        self.compose_bass(track=self.tracks['bass'],
                          channel=self.tracks['bass'])

        self.compose_harmony(track=self.tracks['harmony'],
                             channel=self.tracks['harmony'])

        self.compose_solo(track=self.tracks['solo'],
                          channel=self.tracks['solo'])

        self.compose_percussion(track=self.tracks['percussion'],
                                channel=self.tracks['percussion'])

    def initialize_song(self):
        self.choices()
        self.compose()

    def build_scale(self):

        # intervals_filtered is for solo, while intervals_full is for harmony/bass

        if self.scale_mode == 'minor':
            intervals_filtered = [self.intervals_dic['T'], self.intervals_dic['3m'],
                                  self.intervals_dic['4J'], self.intervals_dic['5J'],
                                  self.intervals_dic['7m']]
        else:
            intervals_filtered = [self.intervals_dic['T'], self.intervals_dic['2M'],
                                  self.intervals_dic['3M'], self.intervals_dic['5J'],
                                  self.intervals_dic['6M']]

        intervals_full = list.copy(intervals_filtered)

        if self.scale_mode == 'minor':
            intervals_full.extend([self.intervals_dic['2M'], self.intervals_dic['6m']])
        else:
            intervals_full.extend([self.intervals_dic['7M'], self.intervals_dic['4J']])

        # Pentablues has an extra interval.
        if self.scale_type == 'pentablues':
            if self.scale_mode == 'minor':
                intervals_filtered.insert(3, intervals_filtered[2] + self.intervals_dic['2m'])
            else:
                intervals_filtered.insert(2, intervals_filtered[1] + self.intervals_dic['2m'])

        # Multiple full octaves with their due intervals.
        self.scale_keyboard_filtered = [None] * (self.num_octaves * len(intervals_filtered))
        self.scale_keyboard_full = [None] * (self.num_octaves * len(intervals_full))

        for idx, interval in enumerate(intervals_filtered):
            for octave in range(0, self.num_octaves):
                self.scale_keyboard_filtered[idx + len(intervals_filtered) * octave] = self.key + interval + octave * 12

        for idx, interval in enumerate(intervals_full):
            for octave in range(0, self.num_octaves):
                self.scale_keyboard_full[idx + len(intervals_full) * octave] = self.key + interval + octave * 12

    def progression_scale_keyboard(self):
        keyboard = list(filter(lambda x: x < self.key + 12, self.scale_keyboard_full))
        return keyboard

    def compose_progression(self):

        local_scale_keyboard = self.progression_scale_keyboard()

        # using bar as unit
        self.progression = []

        if self.progression_type == 'blues':
            for idx_piece in range(0, int(self.num_bars / 12)):
                self.progression.extend([self.key,
                                         self.key,
                                         self.key,
                                         self.key,
                                         self.key + self.intervals_dic['4J'],
                                         self.key + self.intervals_dic['4J'],
                                         self.key,
                                         self.key,
                                         self.key + self.intervals_dic['5J'],
                                         self.key + self.intervals_dic['4J'],
                                         self.key,
                                         self.key + self.intervals_dic['5J']
                                         ])

        if self.progression_type == 'fall':
            if self.scale_mode == 'minor':
                for idx_piece in range(0, int(self.num_bars / 12)):
                    self.progression.extend(3 *
                                            [self.key, self.key - self.intervals_dic['2M'],
                                             self.key - self.intervals_dic['3M'],
                                             self.key - self.intervals_dic['4J']])
            else:
                # I only like this fall for minors
                self.progression_type = 'free'

        if self.progression_type == 'free':

            self.progression.append(self.key)
            composed_bars = 0
            repetitions = np.array([1, 2, 3, 4])
            repetitions_chances = np.array([0.35, 0.40, 0.15, 0.10])
            # repetitions_chances = repetitions / repetitions.sum()

            while composed_bars < self.num_bars - 2:
                repetition = np.random.choice(repetitions, 1, p=repetitions_chances)[0]
                key = random.choice(local_scale_keyboard)
                if composed_bars + repetition > self.num_bars - 2:
                    repetition = self.num_bars - 2 - composed_bars

                for i in range(0, repetition):
                    self.progression.append(key)
                    composed_bars += 1

            self.progression.append(self.key)

    def percussion_scale_keyboard(self):
        keyboard = list(range(self.low_ref1, self.low_ref1 + 24))
        return keyboard

    def compose_percussion(self, track, channel):

        percussion = []
        local_percussion_keyboard = self.percussion_scale_keyboard()
        idx_previous_drum = None
        percussion_timeline = 0

        if self.drummed:

            for bar in range(0, self.num_bars):

                melody_bar = []

                # kick and snare for quaternary
                if self.times == 4:

                    # leave space for opening turn
                    if percussion_timeline > 0:
                        melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1,
                                      'duration': self.beat / 2, 'time': percussion_timeline})
                        melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1 + 2,
                                      'duration': self.beat / 2, 'time': percussion_timeline + self.beat})
                        # space for ending turns
                        if random.uniform(0, 1) <= 0.75:
                            melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1,
                                          'duration': self.beat / 2, 'time': percussion_timeline + self.beat * 2})
                            melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1 + 2,
                                          'duration': self.beat / 2, 'time': percussion_timeline + self.beat * 3})

                # kick and snare for ternary
                if self.times == 3:

                    # leave space for opening turn
                    if percussion_timeline > 0:
                        melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1,
                                      'duration': self.beat / 2, 'time': percussion_timeline})
                        # space for ending turns
                        if random.uniform(0, 1) <= 0.75:
                            melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1 + 2,
                                          'duration': self.beat / 2, 'time': percussion_timeline + self.beat})
                            melody_bar.append({'track': track, 'channel': channel, 'pitch': self.low_ref1 + 2,
                                          'duration': self.beat / 2, 'time': percussion_timeline + self.beat * 2})

                # extras
                percussion_timeline = self.get_melody_bar(melody_bar,
                                                     local_percussion_keyboard,
                                                     track,
                                                     channel,
                                                     percussion_timeline,
                                                     idx_previous_drum)

                percussion.append(melody_bar)

        else:
            percussion.append([{'track': track, 'channel': channel, 'pitch': 0,
                          'duration': 1 / 64, 'time': percussion_timeline}])

        self.genotype['percussion'] = percussion

    def solo_scale_keyboard_filtered(self):

        keyboard = list(filter(lambda x: x >= self.low_ref2
                                     and x <= self.low_ref2 + self.melody_reach,
                        self.scale_keyboard_filtered))
        return keyboard

    def compose_solo(self, track, channel):

        solo = []
        local_scale_keyboard_filtered = self.solo_scale_keyboard_filtered()
        idx_previous_pitch = None
        solo_timeline = 0

        for bar in range(0, self.num_bars):
            melody_bar = []

            # there is a chance of having empty bars
            if random.uniform(0, 1) <= self.silent_bars:
                solo_timeline += self.times * self.beat
                idx_previous_pitch = None
            else:
                solo_timeline = self.get_melody_bar(melody_bar,
                                                    local_scale_keyboard_filtered,
                                                    track,
                                                    channel,
                                                    solo_timeline,
                                                    idx_previous_pitch)
            solo.append(melody_bar)

        self.genotype['solo'] = solo

    def get_melody_bar(self, melody_bar, local_scale_keyboard_filtered, track, channel, melody_timeline, idx_previous_pitch):

        total_time_bar = 0
        while total_time_bar < self.times * self.beat:

            duration = self.get_melody_duration()
            if total_time_bar + duration <= self.times * self.beat:
                pitch, idx_previous_pitch = self.get_melody_pitch(local_scale_keyboard_filtered, idx_previous_pitch)

                # rest is added as a note, but accounts in the timeline
                if pitch != 0:
                    melody_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                       'duration': duration, 'time': melody_timeline})

                total_time_bar = total_time_bar + duration
                melody_timeline = melody_timeline + duration

        return melody_timeline

    def get_melody_duration(self):

        melody_granularity = random.choice(self.melody_granularities)
        duration_pool = np.array([self.duration_pool[value] for value in self.duration_pool])
        idx_distances = np.arange(0, len(self.duration_pool))
        list_distances = abs(idx_distances - np.where(duration_pool == self.beat)[0])
        list_distances = 1 / (list_distances + 1)

        list_distances = pow(list_distances, melody_granularity)
        list_distances = list_distances / list_distances.sum()

        duration = np.random.choice(duration_pool, 1, p=list_distances)[0]

        return duration

    def get_melody_pitch(self, local_scale_keyboard_filtered, idx_previous_pitch):

        if idx_previous_pitch is None:
            idx_pitch = random.choice(range(0, len(local_scale_keyboard_filtered)))
            pitch = local_scale_keyboard_filtered[idx_pitch]
        else:
            idx_distances = np.arange(0, len(local_scale_keyboard_filtered))
            list_distances = abs(idx_distances - idx_previous_pitch)
            list_distances = 1 / (list_distances + 1)
            melody_granularity = random.choice(self.melody_granularities)
            list_distances = pow(list_distances, melody_granularity)

            # pitch repetition happens a little bit more than the average
            # (the plus one above garantees this and avoids division by zero)
            list_distances[np.where(list_distances == 1)] = np.average(list_distances)
            list_distances = list_distances / list_distances.sum()

            # the more distant a pitch, the less likely it is to be selected
            idx_pitch = np.random.choice(idx_distances, 1, p=list_distances)[0]
            pitch = local_scale_keyboard_filtered[idx_pitch]

            # the pitches more than an octave higher than the previous pitch became rests

            if abs(local_scale_keyboard_filtered[idx_pitch] - local_scale_keyboard_filtered[idx_previous_pitch]) > 12:
                # additionally, there is a chance the note becomes a rest anyway???
                # or random.uniform(0, 1) <= 0.15:
                pitch = 0
                idx_pitch = None

        return pitch, idx_pitch

    def compose_bass(self, track, channel):

        bass_timeline = 0
        bass_progression = []

        for pitch in self.progression:

            bass_progression_bar = []
            bass_timeline = self.compose_bass_progression_bar(bass_progression_bar, pitch, track, channel, bass_timeline)
            bass_progression.append(bass_progression_bar)

        self.genotype['bass'] = bass_progression

    def compose_bass_progression_bar(self, bass_progression_bar, pitch, track, channel, bass_timeline):

        # some variations work either only for quaternay or ternary
        if self.times == 3:
            variation = random.choice(range(1, 3 + 1))

        if self.times == 4:
            variation = random.choice(range(2, 7 + 1))

        # waltz (made for ternary)
        if variation == 1:
            duration = self.beat
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration

        # tonic full bar
        if variation == 2:
            duration = self.times * self.beat
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration

        # tonic per beat
        if variation == 3:
            for i in range(0, self.times):
                duration = self.beat
                bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                             'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

        # tonic levadinha (made for quaternary)
        if variation == 4:
            duration = self.beat
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration + self.beat
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration + self.beat / 2
            duration = self.beat / 2
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration

        # tonic eight alternation (made for quaternary)
        if variation == 5:
            duration = self.beat * 2
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['8J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration

        # tonic-fifth alternation  (made for quaternary)
        if variation == 6:
            duration = self.beat * 2
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration

        # tonic-fifth-eight arpeggio  (made for quaternary)
        if variation == 7:
            duration = self.beat
            bass_progression_bar.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['8J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration
            bass_progression_bar.append(
                {'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                 'duration': duration, 'time': bass_timeline})
            bass_timeline = bass_timeline + duration

        return bass_timeline

    def compose_harmony(self, track, channel):

        harmony_timeline = 0
        harmony_progression = []

        for pitch in self.progression:

            chord = []

            # there is a chance first bar is silent
            if harmony_timeline == 0 and random.uniform(0, 1) <= 0.5:
                harmony_timeline += self.times * self.beat
            else:
                harmony_timeline = self.compose_chord(chord, pitch, track, channel, harmony_timeline)

            harmony_progression.append(chord)

        self.genotype['harmony'] = harmony_progression

    def compose_chord(self, chord, pitch, track, channel, harmony_timeline):

        duration = self.times * self.beat

        # harmony should not go as low as bass
        if pitch < self.low_ref2 - 12:
            pitch = pitch + self.intervals_dic['8J']

        chord.append({'track': track, 'channel': channel, 'pitch': pitch,
                      'duration': duration, 'time': harmony_timeline})

        pitch_third = pitch + self.intervals_dic['3m']
        if self.scale_keyboard_full.count(pitch_third) == 0:
            pitch_third += 1

        pitch_fifth = pitch + self.intervals_dic['5J']
        if self.scale_keyboard_full.count(pitch_fifth) == 0:
            pitch_fifth += -1

        chord.append({'track': track, 'channel': channel, 'pitch': pitch_third,
                      'duration': duration, 'time': harmony_timeline})

        chord.append({'track': track, 'channel': channel, 'pitch': pitch_fifth,
                      'duration': duration, 'time': harmony_timeline})
        harmony_timeline = harmony_timeline + duration

        self.inversion(chord)

        return harmony_timeline

    def inversion(self, chord):

        # apply none, fifth, or fifth inversion
        for aux_i in range(0, random.choice([0, 3])):

            # inverts fifth
            if aux_i == 1:
                if chord[2]['pitch'] - 12 >= self.low_ref1:
                    chord[2]['pitch'] = chord[2]['pitch'] - 12
            # inverts third
            if aux_i == 2:
                if chord[2]['pitch'] - 12 >= self.low_ref1:
                    chord[1]['pitch'] = chord[1]['pitch'] - 12

    def get_song_duration(self):

        total_beats = self.beat * self.times * self.num_bars
        minute_portion = total_beats / self.tempo
        seconds = minute_portion * 60
        return seconds

    def build_midi(self, path='', song_id='', export_phenotype=False):

        if self.tracks_granularity == 'track' and export_phenotype:

            for track in self.genotype:
                self.phenotype = MIDIFile(
                    numTracks=len(self.tracks),
                    deinterleave=False)
                self.phenotype.addTempo(0,  # track
                                        0,  # time
                                        self.tempo)
                self.add_notes_midi(track)
                self.export_midi(path+'/phenotypes/'+song_id+'_'+track)

        if self.tracks_granularity == 'all':
            self.phenotype = MIDIFile(
                    numTracks=len(self.tracks),
                    deinterleave=False)
            self.phenotype.addTempo(0,  #track
                                    0,  #time
                                    self.tempo)

            self.add_notes_midi()
            if export_phenotype:
                self.export_midi(path+'/phenotypes/'+song_id)

    def build_karaoke(self):

        num_bars_karaoke = 10
        ini_indx = 0
        fin_indx = num_bars_karaoke
        chords = []

        for chord in self.genotype['harmony']:

            mode = ''

            if len(chord) == 0:
                chords.append('-')
            else:
                if abs(chord[0]['pitch'] - chord[2]['pitch']) % 2 == 0:
                    mode = '°'
                else:
                    if abs(chord[0]['pitch'] - chord[1]['pitch']) % 2 > 0:
                        mode = 'm'

                chord = self.pitch_labels[chord[0]['pitch']] + mode
                chords.append(chord)
        print(self.key)
        print(self.scale_mode)
        print(chords)

        for i in range(0, len(chords), num_bars_karaoke-1):

            chords_sequence = chords[ini_indx:fin_indx]
            if len(chords_sequence) < num_bars_karaoke:
                chords_sequence.extend([''] * (num_bars_karaoke-len(chords_sequence)))
            self.karaoke_chords.append(chords_sequence)

            ini_indx = fin_indx - 1
            if len(chords) - fin_indx < num_bars_karaoke - 1:
                fin_indx = len(chords)
            else:
                fin_indx = fin_indx + num_bars_karaoke - 1

    def add_notes_midi(self, track_export=None):

        for track in self.genotype:
            if track_export is None or track == track_export:
                for bar in range(0, len(self.genotype[track])):
                    for idx_note in range(0, len(self.genotype[track][bar])):
                        self.phenotype.addNote(self.genotype[track][bar][idx_note]['track'],
                                               self.genotype[track][bar][idx_note]['channel'],
                                               self.genotype[track][bar][idx_note]['pitch'],
                                               self.genotype[track][bar][idx_note]['time'],
                                               self.genotype[track][bar][idx_note]['duration'],
                                               self.volumes[track])

    def export_metadata(self):

        pass

    def export_midi(self, name):

        with open(name+'.mid', "wb") as output_file:
            self.phenotype.writeFile(output_file)

    def play_midi(self):

        if self.tracks_granularity == 'all':
            fs = FluidSynth()
            fs.play_midi(self.song_id+'.mid')
        else:
            print('MIDIs were exported track by track, thus will not play.')

