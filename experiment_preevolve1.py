from evolution import *

experiment_name = 'preevolve1'

_num_objectives = 2
_mutation_size = 0.3
_population_size = 10
_generations = 4#10
_cataclysmic_mutations_freqs = 4
_cataclysmic_mutations_size = 2
_max_score = 5
_timeout = 10
_go_live = True
_infinite_generations = False

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
                         _go_live,
                         _infinite_generations
        )

experiment.evolve()
