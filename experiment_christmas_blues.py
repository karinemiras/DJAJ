from evolution import *

experiment_name = 'christmas_jam_blues'

_num_objectives = 2
_mutation_size = 0.5
_population_size = 10
_generations = 0
_cataclysmic_mutations_freqs = 3
_cataclysmic_mutations_size = 5
_max_score = 5
_timeout = 60
_num_bars = 24
# only rpop/rock instruments
_presets = [2, 11, 12, 13, 18, 29, 42, 46, 50]
_go_live = True
_infinite_generations = True
_user_evaluation = True
_progression_type = 'blues'
_times = 4

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
                         _user_evaluation,
                         _progression_type,
                         _times
        )

experiment.evolve()

