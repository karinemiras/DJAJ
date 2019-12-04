from evolution import *

experiment_name = 'exposition'

_num_objectives = 2
_mutation_size = 0.5
_population_size = 30
_generations = 0
_cataclysmic_mutations_freqs = 3
_cataclysmic_mutations_size = 5
_max_score = 5
_timeout = 30
_num_bars = 24
_presets = range(1, 51+1, 1)
_go_live = True
_infinite_generations = True
_user_evaluation = True

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
                         _infinite_generations,
                         _user_evaluation
        )

experiment.evolve()
