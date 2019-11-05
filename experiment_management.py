import os
import shutil
import numpy as np
import pickle
import glob
import sys


class ExperimentManagement:

    def __init__(self, _path):
        self.experiment_folder = _path

    def create_exp_folders(self):
        if os.path.exists(self.experiment_folder):
            shutil.rmtree(self.experiment_folder)
        os.makedirs(self.experiment_folder)
        os.mkdir(self.experiment_folder+'/genotypes')
        os.mkdir(self.experiment_folder+'/phenotypes')
        os.mkdir(self.experiment_folder + '/selectedpop')

        print('Created experiment folders.')

    def export_snapshot(self, population, gen_num):
        # saves a list with all individuals selected for survival in a genration
        file_selected = open(self.experiment_folder+'/selectedpop/selectedpop_'+str(gen_num)+'.txt', 'w')
        for ind in population:
            file_selected.write(ind[0].song_id+'\n')
        file_selected.close()

    def experiment_is_new(self):
        # returns false (not new) is there is any song that has been evaluated and saved as an Individual object
        if not os.path.exists(self.experiment_folder):
            return True
        files = [f for f in glob.glob(self.experiment_folder+'/genotypes/'+"*.pkl")]
        if len(files) == 0:
            return True
        else:
            return False

    def read_recovery_state(self, population_size, offspring_size):

        # discovers which snapshot is the latest if there is any
        snapshots = [f for f in sorted(glob.glob(self.experiment_folder + '/selectedpop/' + "*.txt"))]
        print('pintos',snapshots)
        latest_snapshot = snapshots[-1].split('/selectedpop_')[1].split('.')[0]

        if len(snapshots) > 0:
            # the latest complete snapshot
            last_snapshot = int(latest_snapshot)
            # number of individuals expected until the snapshot
            n_individuals = population_size + last_snapshot * offspring_size
        else:
            last_snapshot = -1
            n_individuals = 0

        individuals_ids = [f for f in sorted(glob.glob(self.experiment_folder + '/genotypes/' + "*.pkl"))]
        print('cuus',individuals_ids)

        latest_id = int(individuals_ids[-1].split('/individual_')[1].split('.')[0])
        print(latest_id)
        # if there are more individuals to recover than the number expected in this snapshot
        if latest_id > n_individuals:
            # then there is a partial offspring
            has_offspring = True
        else:
            has_offspring = False

        return last_snapshot, has_offspring, latest_id

    def load_population(self, population, generation, population_size):
        selectedpop = []
        file = open(self.experiment_folder + '/selectedpop/selectedpop_'+str(generation)+".txt", "r")
        for individual in file:
            selectedpop.append(individual.rstrip('\n'))

        for ind in range(0, population_size):
            with open(self.experiment_folder+'/genotypes/individual_' + selectedpop[ind] + '.pkl', 'rb') as input:
                population[ind] = pickle.load(input)

    def load_offspring(self, offspring, last_snapshot, population_size, offspring_size, latest_id):

        # number of individuals expected until the latest snapshot
        if last_snapshot == -1:
            n_individuals = 0
        else:
            n_individuals = population_size + last_snapshot * offspring_size

        for individual_id in range(n_individuals+1, latest_id+1):
            print('rec',individual_id)
            with open(self.experiment_folder + '/genotypes/individual_' + str(individual_id) + '.pkl', 'rb') as input:
                offspring.append(pickle.load(input))

        amount_recovered = latest_id - n_individuals
        return amount_recovered



