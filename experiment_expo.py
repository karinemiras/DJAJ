from evolution import *

experiment = Evolution(
                        experiment_name='exposition',
                        _num_objectives=2,
                        _mutation_size=0.5,
                        _population_size=10,#30,
                        _generations=0,
                        _cataclysmic_mutations_freqs=3,
                        _cataclysmic_mutations_size=5,
                        _max_score=5,
                        _timeout=2,#15,
                        _num_bars=24,
                        _presets=range(1, 51 + 1, 1),
                        _go_live=True,
                        _infinite_generations=True,
                        _user_evaluation=True,
                        _user_solo=True
        )

experiment.evolve()
