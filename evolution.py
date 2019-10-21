from improvisation import Improvisation
from golive import *
from mutate import *
import copy

for i in range(1, 2):

    song_name = 'song_'+str(i)
    song = Improvisation(song_name)
    song.initialize_song()
    song.build_midi()


    # print('------ original-----')
    # for s in song.genotype['solo']:
    #    print(s)

    replicated_song = copy.deepcopy(song)

    mutate(replicated_song)
    # print('------ kid-----')
    # for s in replicated_song.genotype['solo']:
    #     print(s)
    # print('------ original2-----')
    #
    # for s in song.genotype['solo']:
    #     print(s)

    replicated_song.song_name = 'offsw'
    replicated_song.build_midi()
    replicated_song.export_midi(replicated_song.song_name)

    song.export_midi(song.song_name)