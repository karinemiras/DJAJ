from evolution import Evolution
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--experiment_name', default='default_experiment', help='name of the experiment')
parser.add_argument('--generation', help='generation of the snapshot you wish to hear')
parser.add_argument('--individual', help='id of individual you wanna listen, '
                                         'only used if no snapshot provided')
args = parser.parse_args()


Evolution(args.experiment_name).listen(args.generation,
                                       args.individual)

