import numpy as np
import random

class Initialization:

    def build_scale(self):

        if self.scale_mode == 'minor':
            intervals = [self.intervals_dic['T'], self.intervals_dic['3m'],
                         self.intervals_dic['4J'], self.intervals_dic['5J'],
                         self.intervals_dic['7m']]
        else:
            intervals = [self.intervals_dic['T'], self.intervals_dic['2M'],
                         self.intervals_dic['3M'], self.intervals_dic['5J'],
                         self.intervals_dic['6M']]

        # Pentablues has an extra interval.
        if self.scale_type == 'pentablues':
            if self.scale_mode == 'minor':
                intervals.insert(3, intervals[2] + self.intervals_dic['2m'])
            else:
                intervals.insert(2, intervals[1] + self.intervals_dic['2m'])

        # Multiple full octaves with their due intervals.
        self.scale_keyboard = [None] * (self.num_octaves * len(intervals))

        for idx, interval in enumerate(intervals):
            for octave in range(0, self.num_octaves):
                self.scale_keyboard[idx + len(intervals) * octave] = self.key + interval + octave * 12


    def build_progressions(self):

        # using bar as unit
        self.progression = []
        local_scale_keyboard = list(filter(lambda x: x < self.low_ref2 + 12, self.scale_keyboard))

        # Free has more chance of happening than fixed progressions.
        types = ['blues', 'fall']
        types.extend(['free'] * 4)
        type = random.choice(types)

        if type == 'blues':
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

        if type == 'fall':
            if self.scale_mode == 'minor':
                for idx_piece in range(0, int(self.num_bars / 12)):
                    self.progression.extend(3 *
                                            [self.key, self.key - self.intervals_dic['2M'],
                                             self.key - self.intervals_dic['3M'],
                                             self.key - self.intervals_dic['4J']])
            else:
                # I only like this fall for minors
                type = 'free'

        if type == 'free':
            self.progression.append(self.key)
            for idx_piece in range(0, self.num_bars - 2):
                self.progression.append(random.choice(local_scale_keyboard))
            self.progression.append(self.key)


    def initialize_song(self):

        self.tempo = int(min(max(np.random.normal(self.tempo_pool['mean'], self.tempo_pool['std'], 1)[0],
                                 self.tempo_pool['min']),
                             self.tempo_pool['max']))
        self.key = random.choice(self.pitch_pool)
        self.scale_mode = random.choice(self.scale_modes)
        self.scale_type = random.choice(self.scale_types)
        self.melody_granularity = random.choice(self.melody_granularities)
        self.times = random.choice(self.times_pool)
        self.max_time_line = self.num_bars * self.times * self.beat
        self.define_instruments()

        # no drumming for ternary
        if self.times == 3:
            self.drummed = False
        else:
            self.drummed = True if random.uniform(0, 1) <= self.drummed_prob else False

        self.build_pitch_labels()
        self.build_scale()

        self.build_progressions()

        self.compose_bass(track=self.tracks['bass'],
                          channel=self.tracks['bass'])

        self.compose_chords(track=self.tracks['chords'],
                            channel=self.tracks['chords'])

        self.compose_solo(track=self.tracks['solo'],
                          channel=self.tracks['solo'])

        self.compose_drums(track=self.tracks['drums'],
                           channel=self.tracks['drums'])

        self.build_midi()


    def define_instruments(self):
        self.instruments = random.choice(self.instruments)


    def compose_drums(self, track, channel):

        drums = []
        local_drums_keyboard = list(range(self.low_ref1, self.low_ref1 + 24))
        idx_previous_drum = None
        drums_timeline = 0

        if self.drummed:

            for bar in range(0, self.num_bars):

                # kick and snare for quaternary
                if self.times == 4:

                    # leave space for opening turn
                    if drums_timeline > 0:
                        drums.append({'track': track, 'channel': channel, 'pitch': self.low_ref1,
                                      'duration': self.beat / 2, 'time': drums_timeline})
                        drums.append({'track': track, 'channel': channel, 'pitch': self.low_ref1 + 2,
                                      'duration': self.beat / 2, 'time': drums_timeline + self.beat})
                        # space for ending turns
                        if random.uniform(0, 1) <= 0.75:
                            drums.append({'track': track, 'channel': channel, 'pitch': self.low_ref1,
                                          'duration': self.beat / 2, 'time': drums_timeline + self.beat * 2})
                            drums.append({'track': track, 'channel': channel, 'pitch': self.low_ref1 + 2,
                                          'duration': self.beat / 2, 'time': drums_timeline + self.beat * 3})

                # extras
                drums_timeline = self.get_melody_bar(drums,
                                                     local_drums_keyboard,
                                                     track,
                                                     channel,
                                                     drums_timeline,
                                                     idx_previous_drum)

        else:
            drums.append({'track': track, 'channel': channel, 'pitch': 0,
                          'duration': 1/64, 'time': drums_timeline})

        self.genotype['drums'] = drums


    def compose_solo(self, track, channel):

        solo = []
        local_scale_keyboard = list(filter(lambda x: x >= self.low_ref2
                                                     and x <= self.low_ref2 + self.melody_reach,
                                           self.scale_keyboard))
        idx_previous_pitch = None
        solo_timeline = 0

        for bar in range(0, self.num_bars):

            # there is a chance of having empty bars
            if random.uniform(0, 1) <= self.silent_bars:
                solo_timeline += self.times * self.beat
            else:
                solo_timeline = self.get_melody_bar(solo,
                                                    local_scale_keyboard,
                                                    track,
                                                    channel,
                                                    solo_timeline,
                                                    idx_previous_pitch)

        self.genotype['solo'] = solo


    def get_melody_bar(self, melody, local_scale_keyboard, track, channel, melody_timeline, idx_previous_pitch):

        total_time_bar = 0
        while total_time_bar < self.times * self.beat:

            duration = self.get_melody_duration()
            if total_time_bar + duration <= self.times * self.beat:
                pitch, idx_previous_pitch = self.get_melody_pitch(local_scale_keyboard, idx_previous_pitch)

                # rest is added as a note, but accounts in the timeline
                if pitch != 0:
                    melody.append({'track': track, 'channel': channel, 'pitch': pitch,
                                   'duration': duration, 'time': melody_timeline})

                total_time_bar = total_time_bar + duration
                melody_timeline = melody_timeline + duration

        return melody_timeline


    def get_melody_duration(self):

        duration_pool = np.array([self.duration_pool[value] for value in self.duration_pool])
        idx_distances = np.arange(0, len(self.duration_pool))
        list_distances = abs(idx_distances - np.where(duration_pool == self.beat)[0])
        list_distances = 1 / (list_distances + 1)
        list_distances = pow(list_distances, self.melody_granularity)
        list_distances = list_distances / list_distances.sum()

        duration = np.random.choice(duration_pool, 1, p=list_distances)[0]

        return duration


    def get_melody_pitch(self, local_scale_keyboard, idx_previous_pitch):

        if idx_previous_pitch is None:
            idx_pitch = random.choice(range(0, len(local_scale_keyboard)))
            pitch = local_scale_keyboard[idx_pitch]
        else:
            idx_distances = np.arange(0, len(local_scale_keyboard))
            list_distances = abs(idx_distances - idx_previous_pitch)
            list_distances = 1 / (list_distances + 1)
            list_distances = list_distances * list_distances

            # pitch repetition happens a little bit more than the average
            # (the plus one above garantees this and avoids division by zero)
            list_distances[np.where(list_distances == 1)] = np.average(list_distances)
            list_distances = list_distances / list_distances.sum()

            # the more distant a pitch, the less likely it is to be selected
            idx_pitch = np.random.choice(idx_distances, 1, p=list_distances)[0]
            pitch = local_scale_keyboard[idx_pitch]

            # the pitches more than an octave higher than the previous pitch became rests

            if abs(local_scale_keyboard[idx_pitch] - local_scale_keyboard[idx_previous_pitch]) > 12:
                # additionally, there is a chance the note becomes a rest anyway???
                # or random.uniform(0, 1) <= 0.15:
                pitch = 0
                idx_pitch = None

        return pitch, idx_pitch


    def compose_bass(self, track, channel):

        bass_timeline = 0
        bass_progression = []

        for pitch in self.progression:

            # some variations work either only for quaternay or ternary
            if self.times == 3:
                variation = random.choice(range(1, 3 + 1))

            if self.times == 4:
                variation = random.choice(range(2, 7 + 1))

            # waltz (made for ternary)
            if variation == 1:
                duration = self.beat
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

            # tonic full bar
            if variation == 2:
                duration = self.times * self.beat
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

            # tonic per beat
            if variation == 3:
                for i in range(0, self.times):
                    duration = self.beat
                    bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                             'duration': duration, 'time': bass_timeline})
                    bass_timeline = bass_timeline + duration

            # tonic levadinha (made for quaternary)
            if variation == 4:
                duration = self.beat
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration + self.beat
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration + self.beat / 2
                duration = self.beat / 2
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

            # tonic eight alternation (made for quaternary)
            if variation == 5:
                duration = self.beat * 2
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['8J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

            # tonic-fifth alternation  (made for quaternary)
            if variation == 6:
                duration = self.beat * 2
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

            # tonic-fifth-eight arpeggio  (made for quaternary)
            if variation == 7:
                duration = self.beat
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch,
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['8J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration
                bass_progression.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                                         'duration': duration, 'time': bass_timeline})
                bass_timeline = bass_timeline + duration

        self.genotype['bass'] = bass_progression


    def compose_chords(self, track, channel):

        chords_timeline = 0
        chords_progression = []

        duration = self.times * self.beat
        for pitch in self.progression:

            chord = []
            # chords should not go as low as bass
            if pitch < self.low_ref2 - 12:
                pitch = pitch + self.intervals_dic['8J']

            # there is a chance first bar is silent
            if chords_timeline == 0 and random.uniform(0, 1) <= 0.5:
                chords_timeline += self.times * self.beat
            else:
                chord.append({'track': track, 'channel': channel, 'pitch': pitch,
                              'duration': duration, 'time': chords_timeline})

                pitch_third = pitch + self.intervals_dic['3m']
                if self.scale_keyboard.count(pitch) == 0:
                    pitch_third += 1
                chord.append({'track': track, 'channel': channel, 'pitch': pitch_third,
                              'duration': duration, 'time': chords_timeline})

                chord.append({'track': track, 'channel': channel, 'pitch': pitch + self.intervals_dic['5J'],
                              'duration': duration, 'time': chords_timeline})
                chords_timeline = chords_timeline + duration

                self.inversion(chord)

                chords_progression.extend(chord)

        self.genotype['chords'] = chords_progression


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

