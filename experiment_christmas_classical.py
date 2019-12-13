from evolution import *

# only classic and chill ones: no keyboard soling, neither distorted guitar

experiment = Evolution(
                        experiment_name='christmas_jam_classical',
                        _num_objectives=2,
                        _mutation_size=0.5,
                        _population_size=10,
                        _generations=2,
                        _cataclysmic_mutations_freqs=0,
                        _cataclysmic_mutations_size=0,
                        _max_score=5,
                        _timeout=60,
                        _num_bars=24,
                        _presets=[  16, 17, 25, 26, 28,
                                    30, 31, 32, 33, 34, 35, 36,
                                    37, 38, 41, 43, 44, 45, 47,
                                    48, 49],
                        _tempo_pool={'min': 90, 'mean': 120, 'std': 10, 'max': 160},
                        _silent_bars_range=[0.3, 0.6],
                        _go_live=True,
                        _infinite_generations=False,
                        _user_evaluation=True,
        )

experiment.evolve()

