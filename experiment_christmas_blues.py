from evolution import *

# all the non classical instruments
classical = [16, 17, 25, 26, 28,
            30, 31, 32, 33, 34, 35, 36,
            37, 38, 41, 43, 44, 45, 47,
            48, 49]
all = list(range(1, 51+1, 1))
nonclassical = [x for x in all if x not in classical]

experiment = Evolution(
                        experiment_name='christmas_jam_blues',
                        _num_objectives=2,
                        _mutation_size=0.5,
                        _population_size=10,
                        _generations=2,
                        _cataclysmic_mutations_freqs=0,
                        _cataclysmic_mutations_size=0,
                        _max_score=5,
                        _timeout=60,
                        _num_bars=24,
                        _presets=nonclassical,
                        _go_live=True,
                        _infinite_generations=False,
                        _user_evaluation=True,
                        _progression_type='blues',
                        _times=4

)

experiment.evolve()

