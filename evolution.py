from song import Song
from golive import *
from mutate import *
from experiment_management import *
from user_input import *

from deap import base
from deap import creator
from deap import tools

import copy
import matplotlib.pyplot as plt
import numpy as np
from pprint import pprint
import shutil


class Evolution:

    def __init__(self, experiment_name,
                 _num_objectives=2,
                 _mutation_size=0.3,
                 _population_size=10,
                 _generations=10,
                 _cataclysmic_mutations_freqs=2,
                 _cataclysmic_mutations_size=2,
                 _max_score=5,
                 _timeout=10,
                 _go_live=True,
                 _infinite_generations=False):

        self.experiment_name = experiment_name

        self.num_objectives = _num_objectives
        self.mutation_size = _mutation_size
        self.population_size = _population_size
        self.generations = _generations
        self.cataclysmic_mutations_freqs = _cataclysmic_mutations_freqs
        self.cataclysmic_mutations_size = _cataclysmic_mutations_size
        self.max_score = _max_score
        self.timeout = _timeout
        self.go_live = _go_live
        self.infinite_generations = _infinite_generations

        self.population = None
        self.offspring = None
        self.next_song_id = None
        self.logbook = None
        self.export_genotype = True
        self.export_phenotype = False
        self.path = 'experiments/' + self.experiment_name

        # values[0]: fitness_quality, values[1]:fitness_novelty
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

        stats_quality = tools.Statistics(lambda ind: ind.fitness.values[0])
        stats_novelty = tools.Statistics(lambda ind: ind.fitness.values[1])
        self.stats = tools.MultiStatistics(quality=stats_quality, novelty=stats_novelty)
        self.stats.register("avg", np.mean, axis=0)
        self.stats.register("std", np.std, axis=0)
        self.stats.register("max", np.max, axis=0)

    def read_logbook(self):
        with open(self.path+'/evolution_summary.pkl', 'rb') as input:
            self.logbook = pickle.load(input)
            print(self.logbook)

    def initialize(self, individual, next_song_id, generation=None, bkp=False):
        individual[0].song_id = str(next_song_id)
        individual[0].initialize_song()
        individual[0].build_midi(self.path, individual[0].song_id, self.export_phenotype)
        self.evaluate(individual, generation, bkp)

    def new_genotype(self):
        song = Song()
        return song

    def new_offspring(self, individual):
        offspring = self.replicate_mutate(individual)
        offspring[0].song_id = str(self.next_song_id)
        self.next_song_id += 1
        offspring[0].build_midi(self.path, offspring[0].song_id, self.export_phenotype)
        self.evaluate(offspring)
        return offspring

    def export_pickle(self, individual, file):
        with open(file, 'wb') as output:
            pickle.dump(individual, output, pickle.HIGHEST_PROTOCOL)

    def logs_results(self, generation, new=True):

        if new:
            self.logbook = tools.Logbook()
            self.logbook.header = "gen", "quality", "novelty"
            self.logbook.chapters["quality"].header = "avg", "std", "max"
            self.logbook.chapters["novelty"].header = "avg", "std", "max"

        record = self.stats.compile(self.population)
        self.logbook.record(gen=generation, **record)
        print('\n'+self.logbook.stream)

        with open(self.path + '/evolution_summary.pkl', 'wb') as output:
            pickle.dump(self.logbook, output, pickle.HIGHEST_PROTOCOL)

    def evaluate(self, individual, generation=None, bkp=False):

        fitness_quality = -1
        fitness_novelty = -1

        individual[0].export_midi('current_song_all')
        if self.go_live:
            went_live = False
            while not went_live:
                went_live = go_live_ableton(individual[0])

            fitness_quality = get_user_input(self.max_score, self.timeout)

        # fix!
        #fitness_novelty = random.uniform(0, 1)

        # values[0]: fitness_quality, values[1]:fitness_novelty
        individual.fitness.values = fitness_quality, fitness_novelty

        if self.export_genotype:
            file = self.path + '/genotypes/individual_' + individual[0].song_id

            # in case of cataclysmic mutation, bkps up original genotype
            if bkp:
                shutil.copyfile(file + '.pkl', file + '_' + str(generation) + '.pkl')

            self.export_pickle(individual, file + '.pkl')

        print('-- evaluated song '+individual[0].song_id +
              ', quality: '+str(fitness_quality)+' novelty: '+str(fitness_novelty))

    def replicate_mutate(self, individual):
        offspring = copy.deepcopy(individual)
        mutate(offspring[0], self.mutation_size)
        return offspring

    def select(self):
        # inserts offspring into population and selects in steady-state
        self.population = self.population + self.offspring
        self.population = self.toolbox.select(self.population)

    def plots_summary(self):

        gen = self.logbook.select("gen")
        quality_avg = self.logbook.chapters["quality"].select("avg")
        quality_std = self.logbook.chapters["quality"].select("std")
        novelty_avg = self.logbook.chapters["novelty"].select("avg")
        novelty_std = self.logbook.chapters["novelty"].select("std")

        fig, ax1 = plt.subplots()
        ax1.plot(gen, quality_avg, "b-", label="Quality")
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Quality", color="b")
        for tl in ax1.get_yticklabels():
            tl.set_color("b")

        ax1.fill_between(gen, np.array(quality_avg) - np.array(quality_std),
                         np.array(quality_avg) + np.array(quality_std), alpha=0.2, facecolor='#66B2FF')

        ax2 = ax1.twinx()
        ax2.plot(gen, novelty_avg, "r-", label="Novelty")
        ax2.set_ylabel("Novelty", color="r")
        for tl in ax2.get_yticklabels():
            tl.set_color("r")

        ax2.fill_between(gen, np.array(novelty_avg) - np.array(novelty_std),
                         np.array(novelty_avg) + np.array(novelty_std), alpha=0.2, facecolor='#FF9999')

        plt.savefig(self.path + '/evolution_summary.png')

    def get_indices_of_k_smallest(self, array, k):
        idx = np.argpartition(array.ravel(), k)
        return tuple(np.array(np.unravel_index(idx, array.shape))[:, range(min(k, 0), max(k, 0))])

    def cataclysmic_mutations(self, generation):

        # replaces the worst individuals for new random ones
        quality = []
        for ind in self.population:
            quality.append(float(ind.fitness.values[0]))

        indexes = np.array(quality).argsort()[-self.cataclysmic_mutations_size:][::1]

        for index in indexes:
            new_genotype = self.toolbox.population(n=1)[0]
            # new genotype keeps id of the pseudo parent
            self.initialize(new_genotype, self.population[index][0].song_id, generation, bkp=True)
            self.population[index] = new_genotype

    def evolve(self):

        experiment_management = ExperimentManagement(self.path)

        do_recovery = not experiment_management.experiment_is_new()
        self.population = self.toolbox.population()

        if do_recovery:

            latest_snapshot, has_offspring, latest_id = experiment_management.read_recovery_state(self.population_size,
                                                                                                  self.population_size)
            generation = latest_snapshot
            self.next_song_id = latest_id + 1

            if latest_snapshot == self.generations - 1:
                print('\nExperiment is already complete.')
                return

            # if there is a snapshot to recover
            if latest_snapshot != -1:
                experiment_management.load_population(self.population, latest_snapshot, self.population_size)
                print('\nSnapshot '+str(latest_snapshot)+' loaded.')

            # if there is a offspring to recover
            if has_offspring:
                self.offspring = self.toolbox.population()
                offspring_recovered = experiment_management.load_offspring(self.offspring, latest_snapshot,
                                                                           self.population_size,
                                                                           self.population_size, latest_id)

                # it recovered offspring is from the first (unfinished) snapshot,
                # fill ups the first population
                if latest_snapshot == -1:

                    generation = 0
                    print('\n----------- GEN: ', generation)

                    for ind in range(offspring_recovered, self.population_size):
                        self.initialize(self.offspring[ind], self.next_song_id)
                        self.next_song_id += 1
                    self.population = self.offspring

                    experiment_management.export_snapshot(self.population, generation)
                    self.logs_results(generation)

                # if there is any finished snapshot, fills up unfinished offspring
                else:

                    self.read_logbook()

                    generation += 1
                    print('\n----------- GEN: ', generation)

                    for ind in range(offspring_recovered, self.population_size):
                        self.offspring[ind] = self.new_offspring(self.population[ind])
                    self.select()

                    experiment_management.export_snapshot(self.population, generation)
                    self.logs_results(generation, new=False)

        else:

            # starting a new experiment
            experiment_management.create_exp_folders()
            generation = 0
            self.next_song_id = 1

            print('\n----------- GEN: ', generation)

            for ind in self.population:
                self.initialize(ind, self.next_song_id)
                self.next_song_id += 1

            experiment_management.export_snapshot(self.population, generation)
            self.logs_results(generation)

        generation += 1

        while generation < self.generations:

            print('\n----------- GEN: ', generation)

            self.offspring = []

            for ind in range(0, self.population_size):
                self.offspring.append(self.new_offspring(self.population[ind]))

            self.select()

            if self.cataclysmic_mutations_freqs > 0:
                if (generation+1) % self.cataclysmic_mutations_freqs == 0:
                    print('\nCataclysmic mutations!')
                    self.cataclysmic_mutations(generation)

            experiment_management.export_snapshot(self.population, generation)

            if do_recovery:
                self.read_logbook()
                do_recovery = False
            self.logs_results(generation, new=False)

            generation += 1

            self.plots_summary()

    def listen(self, generation, song_id):

        if generation is None and song_id is None:
            print('Choose a snapshot or individual!')
            return

        # if there is no snapshot, but there is an individual, plays it
        if generation is not None:
            file = open(self.path + '/selectedpop/selectedpop_' + str(generation) + ".txt", "r")
            for individual in file:
                self.listen_individual(individual.rstrip('\n'))
        else:
            self.listen_individual(song_id)

    def listen_individual(self, song_id):

        individual = song_id
        with open('experiments/' + self.experiment_name + '/genotypes/individual_' + str(individual) + '.pkl',
                  'rb') as input:
            song = pickle.load(input)
            song = song[0]
            pprint(vars(song))

            song.build_midi()
            song.export_midi('current_song_all')
            went_live = False
            while not went_live:
                went_live = go_live_ableton(song)



