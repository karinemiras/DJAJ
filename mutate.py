import copy
import numpy as np
import random


# all genotypes get mutate for 30 percent of the mutable traits
def mutate(song):

    #if np.random.normal(0, 1, 1)[0] <= song.mutation_magnitude:

    if True:
        mutate_tempo(song)

    if True:
        mutate_preset(song)

    if True:
        new_melody_bar(song, 'solo')

    if True:
        new_melody_bar(song, 'drums')

    if True:
        symmetric_melody_bar(song)


def mutate_tempo(song):

    perturb = np.random.normal(0, 20, 1)[0]
    song.tempo = int(min(max(song.tempo + perturb,
                             song.tempo_pool['min']),
                         song.tempo_pool['max']))


def mutate_preset(song):
    song.preset = random.choice(song.presets)


def new_melody_bar(song, track):

    if track == 'solo':
        local_scale_keyboard = song.solo_scale_keyboard()
    if track == 'drums':
        local_scale_keyboard = song.drums_scale_keyboard()

    bar = random.choice(range(0, song.num_bars))
    melody_timeline = bar * song.times * song.beat

    if bar > 0 and len(song.genotype[track][bar-1]) > 0:
        idx_previous_pitch = song.genotype[track][bar-1][-1]['pitch']
        idx_previous_pitch = local_scale_keyboard.index(idx_previous_pitch)
    else:
        idx_previous_pitch = None

    melody_bar = []
    song.get_melody_bar(melody_bar,
                        local_scale_keyboard,
                        song.tracks[track],
                        song.tracks[track],
                        melody_timeline,
                        idx_previous_pitch)

    song.genotype[track][bar] = melody_bar


def symmetric_melody_bar(song):
    track = 'solo'
    type_symmetry = random.uniform(0, 1)

    bar_content = []
    while len(bar_content) == 0:
        bar = random.choice(range(0, song.num_bars - 1))
        bar_content = song.genotype[track][bar]

        # if bar is not silent
        if len(bar_content) > 0:
            song.genotype[track][bar+1] = []

            # repeats bar identically
            if type_symmetry <= 0.5:
                for note in bar_content:
                    song.genotype[track][bar+1].append({'track': note['track'],
                                                        'channel': note['channel'],
                                                        'pitch':  note['pitch'],
                                                        'duration':  note['duration'],
                                                        'time': note['time'] + song.times * song.beat})
            # repeats bar invertedly
            if type_symmetry > 0.5:
                bar_content_inverted = copy.copy(bar_content)[::-1]
                bar_time = (bar+1) * song.times * song.beat
                for note in bar_content_inverted:
                    song.genotype[track][bar+1].append({'track': note['track'],
                                                        'channel': note['channel'],
                                                        'pitch':  note['pitch'],
                                                        'duration':  note['duration'],
                                                        'time': bar_time})
                    bar_time += note['duration']







