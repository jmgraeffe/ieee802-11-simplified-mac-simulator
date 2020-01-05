import logging
import sys
import pickle
from datetime import datetime
from multiprocessing import cpu_count

from common_functions import ensure_dir
import simulation as simulator
from exporters import station_collision_plot, stations_transmissions_plot, iterations_transmissions_plot, iteration_syncnodes_plot

"""TODO
- better export system
- implement averaging in run_multiple in order to increase paralellism (current run_multiple_averaged is basically just a quick workaround hack)
- documentation
- extended commentary
"""


def station_plots(path):
    schemes_markers = {
        simulator.Scheme.DCF_BASIC: dict(marker='s', linestyle=':'),
        simulator.Scheme.CRB: dict(marker='o', linestyle='--'),
        simulator.Scheme.TBRI: dict(marker='^', linestyle='-'),
    }

    range_stations = range(10, 50 + 1, 5)
    # range_stations = range(10, 15)
    # num_iterations = 1000
    num_iterations = 1000000
    # num_simulations = 1
    num_simulations = 16

    simulations = simulator.run_multiple_averaged(num_simulations, [num_iterations], schemes_markers.keys(), range_stations)

    """with open(ensure_dir(path + 'station_simulations.pickle'), 'wb') as file:
        pickle.dump(simulations, file, protocol=pickle.HIGHEST_PROTOCOL)
    """

    station_collision_plot.export(simulations[num_iterations], ensure_dir(path + 'stations_collisions_plot.pdf'), schemes_markers)
    stations_transmissions_plot.export(simulations[num_iterations], ensure_dir(path + 'stations_transmissions_plot.pdf'), schemes_markers)


def iteration_plots(path):
    schemes_markers = {
        simulator.Scheme.DCF_BASIC: dict(marker='s', linestyle=':'),
        simulator.Scheme.CRB: dict(marker='o', linestyle='--'),
        simulator.Scheme.TBRI: dict(marker='^', linestyle='-'),
    }

    stations_schemes_markers = {
        10: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-'),
            simulator.Scheme.TBRI: dict(marker='', linestyle='--'),
        },
        16: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-'),
            simulator.Scheme.TBRI: dict(marker='', linestyle='--'),
        }
    }

    # range_stations = [10]
    range_stations = [16]
    # range_stations = range(8, 16 + 1, 8)
    range_iterations = [300] + list(range(3000, 300000 + 1, 3000))
    # range_iterations = [1500]
    # range_iterations = [15000]
    # num_simulations = 1
    num_simulations = 16

    simulations = simulator.run_multiple_averaged(num_simulations, range_iterations, schemes_markers.keys(), range_stations)

    iterations_transmissions_plot.export(simulations, ensure_dir(path + 'iterations_transmissions_plot.pdf'), schemes_markers)
    # iteration_syncnodes_plot.export(simulations[range_iterations[0]], ensure_dir(path + 'iteration_syncnodes_plot.pdf'), stations_schemes_markers)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout, format='%(message)s')
    print(cpu_count())
    path = 'output/{}/'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    import random
    # random.seed(2)
    random.seed(3050)

    # station_plots(path)
    iteration_plots(path)
