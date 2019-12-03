from evolution import *

experiment_name = 'christmas'

_num_objectives = 2
_mutation_size = 0.5
_population_size = 10
_generations = 0
_cataclysmic_mutations_freqs = 10
_cataclysmic_mutations_size = 2
_max_score = 5
_timeout = 60
_num_bars = 48
# only classic and chill ones: no keyboard soling, neither distorted guitar
_presets = [16, 17, 18, 25, 26, 28,
            30, 31, 32, 33, 34, 35, 36,
            37, 38, 41, 43, 44, 45, 47,
            48, 49]
_go_live = True
_infinite_generations = True

experiment = Evolution(
                         experiment_name,
                         _num_objectives,
                         _mutation_size,
                         _population_size,
                         _generations,
                         _cataclysmic_mutations_freqs,
                         _cataclysmic_mutations_size,
                         _max_score,
                         _timeout,
                         _num_bars,
                         _presets,
                         _go_live,
                         _infinite_generations
        )

experiment.evolve()
