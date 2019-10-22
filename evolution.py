from improvisation import Improvisation
from golive import *
from mutate import *
import copy
import pickle

for i in range(1, 2):

    song_name = 'song_'+str(i)
    song = Improvisation(song_name)
    song.initialize_song()
    song.build_midi()
    song.export_midi('current_song_all')

    replicated_song = copy.deepcopy(song)

    mutate(replicated_song)

    replicated_song.song_name = 'offsw'
    replicated_song.build_midi()
    replicated_song.export_midi(replicated_song.song_name)
    replicated_song.export_midi('current_song_all')
    song.export_midi(song.song_name)



    # with open('company_data.pkl', 'wb') as output:
    #     pickle.dump(song, output, pickle.HIGHEST_PROTOCOL)
    #
    #
    # del song
    #
    #
    # with open('company_data.pkl', 'rb') as input:
    #     company1 = pickle.load(input)
    #     print(company1.tempo)
