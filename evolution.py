from song import Song
from golive import *
from mutate import *

import copy
import pickle



from deap import base
from deap import creator
from deap import tools



class Evolution:

    def __init__(self):

        # fitness1 is quality, and fitness2 is novelty
        self.num_objectives = 2

        creator.create("FitnessesMax", base.Fitness, weights=(1.0,) * self.num_objectives)

        creator.create("Individual", list, fitness=creator.FitnessesMax)

        self.toolbox = base.Toolbox()

        self.toolbox.register("genotype", self.initialize)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                              self.toolbox.genotype, 1)

        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", self.evaluate)

        self.toolbox.register("select", tools.selNSGA2, k=5)

        self.mutation_size = 0.3

    def initialize(self):

        song_name = str(random.choice(range(1, 100)))
        song = Song(song_name)
        song.initialize_song()

        return song

    def evaluate(self, population):

        return random.uniform(0, 1), random.uniform(0, 1)

    def replicate_mutate(self, population):

        offspring = list(map(self.toolbox.clone, population))
        for ind in offspring:
            mutate(ind[0], self.mutation_size)

        return offspring

    def evolve(self):

        population = self.toolbox.population(n=5)

        fitnesses = list(map(self.toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            print(ind[0].tempo)
            ind.fitness.values = fit
        print('--------')
        offspring = self.replicate_mutate(population)

        fitnesses = list(map(self.toolbox.evaluate, offspring))
        for ind, fit in zip(offspring, fitnesses):
            print(ind[0].tempo)
            ind.fitness.values = fit


        population = population + offspring

        print('--------')
        for ind in population:
            print(ind[0].tempo)

        population = self.toolbox.select(population)
        print('--------')
        for ind in population:
            print(ind[0].tempo)

        # for i in range(1, 2):
        #
        #     song_name = 'song_'+str(i)
        #     song = Song(song_name)
        #     song.initialize_song()
        #
        #     song.build_midi()
        #     song.export_midi('current_song_all')

            # went_live = False
            #
            # while not went_live:
            #     went_live = go_live_ableton(song)


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


Evolution().evolve()
