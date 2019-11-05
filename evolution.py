from song import Song
from golive import *
from mutate import *
from experiment_management import *

from deap import base
from deap import creator
from deap import tools
import copy

import numpy as np

#temp
import time

class Evolution:

    def __init__(self, experiment_name):

        self.experiment_name = experiment_name
        self.path = 'experiments/' + self.experiment_name
        self.population = None
        self.offspring = None
        self.next_song_id = None

        # params #
        self.num_objectives = 2
        self.mutation_size = 0.3
        self.population_size = 4
        self.generations = 3#50
        # params #

        self.export_genotype = True
        self.export_phenotype = False
        self.infinite_generations = False
        self.go_live = False

        creator.create("FitnessesMax",
                       base.Fitness,
                       weights=(1.0,) * self.num_objectives)

        creator.create("Individual",
                       list,
                       fitness=creator.FitnessesMax)

        self.toolbox = base.Toolbox()

        self.toolbox.register("genotype", self.new_genotype)

        self.toolbox.register("individual", tools.initRepeat,
                              creator.Individual,
                              self.toolbox.genotype, 1)

        self.toolbox.register("population",
                              tools.initRepeat,
                              list,
                              self.toolbox.individual,
                              n=self.population_size)

        self.toolbox.register("select",
                              tools.selNSGA2,
                              k=self.population_size)

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", np.mean, axis=0)
        self.stats.register("std", np.std, axis=0)

        self.logbook = tools.Logbook()
        self.logbook.header = "gen", "avg", "std"

    def new_genotype(self):
        song = Song('')
        return song

    def new_offspring(self, individual):
        self.offspring.append(self.replicate_mutate(individual))
        self.offspring[-1][0].song_id = str(self.next_song_id)
        self.next_song_id += 1
        self.offspring[-1][0].build_midi(self.path, self.offspring[-1][0].song_id, self.export_phenotype)
        self.evaluate(self.offspring[-1])

    def export_pickle(self, individual, file):

        with open(file, 'wb') as output:
            pickle.dump(individual, output, pickle.HIGHEST_PROTOCOL)

    def evaluate(self, individual):

        individual[0].export_midi(self.path + '/current_song_all')
        if self.go_live:
            went_live = False
            while not went_live:
                went_live = go_live_ableton(individual[0])

        fitness_quality = random.uniform(0,1)
        fitness_novelty = individual[0].tempo

        individual.fitness.values = fitness_quality, fitness_novelty

        time.sleep(1)
        if self.export_genotype:
            self.export_pickle(individual,
                               self.path + '/genotypes/individual_' + individual[0].song_id + '.pkl')

        print('-- evaluated song '+individual[0].song_id +
              ', quality: '+str(fitness_quality)+' novelty: '+str(fitness_novelty))

    def replicate_mutate(self, individual):
        offspring = copy.deepcopy(individual)
        mutate(offspring[0], self.mutation_size)
        return offspring

    def evolve(self):

        experiment_management = ExperimentManagement(self.path)

        do_recovery = not experiment_management.experiment_is_new()
        print(do_recovery)
        self.population = self.toolbox.population()

        if do_recovery:
            generation, has_offspring, latest_id = experiment_management.read_recovery_state(self.population_size,
                                                                                             self.population_size)
            self.next_song_id = latest_id + 1

            if generation == self.generations - 1:
                print('Experiment is already complete.')
                return

            experiment_management.load_population(self.population, generation, self.population_size)

            for ind in self.population:
               print(ind[0].song_id, ind.fitness)

            print('temoff',has_offspring)

            if has_offspring:
                self.offspring = []
                amount_recovered = experiment_management.load_offspring(self.offspring, generation, self.population_size,
                                                                        self.population_size, latest_id)
                generation += 1
                print('----------- GEN: ', generation)

                print('red',amount_recovered)

                for ind in range(amount_recovered, len(self.population)):
                    self.new_offspring(self.population[ind])

                for ind in self.offspring:
                   print(ind[0].song_id, ind.fitness)

        else:
            # starting a new experiment
            experiment_management.create_exp_folders()
            generation = 0
            self.next_song_id = 1

            print('----------- GEN: ', generation)

            for ind in self.population:
                ind[0].song_id = str(self.next_song_id)
                self.next_song_id += 1
                ind[0].initialize_song()
                ind[0].build_midi(self.path, ind[0].song_id, self.export_phenotype)
                self.evaluate(ind)

            experiment_management.export_snapshot(self.population, generation)

            record = self.stats.compile(self.population)
            self.logbook.record(gen=generation, **record)
            print(self.logbook.stream)


        generation += 1

        #
        # file_summary = open(self.path + '/evolution_summary.txt', 'a')
        #
        # file_summary.write('')
        #

        while generation < self.generations:

            print('----------- GEN: ', generation)

            self.offspring = []
            for ind in self.population:
                self.new_offspring(ind)

            record = self.stats.compile(self.population)
            self.logbook.record(gen=generation, **record)
            print(self.logbook.stream)

            # inserts offspring into population and selects in steady-state
            self.population = self.population + self.offspring
            self.population = self.toolbox.select(self.population)

            experiment_management.export_snapshot(self.population, generation)

            generation += 1


       # file_summary.close()

Evolution('test').evolve()
