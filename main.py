import logging
import sys
import time
from datetime import datetime
from multiprocessing import cpu_count

from common_functions import ensure_dir
import simulation as simulator
from exporters import station_collision_plot, stations_transmissions_plot, iterations_transmissions_plot, iteration_syncnodes_plot

"""TODO
- average calculations
- better export system
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

    simulations = simulator.run_multiple([1000000], schemes_markers.keys(), range_stations)

    station_collision_plot.export(simulations, ensure_dir(path + 'stations_collisions_plot.pdf'), schemes_markers)
    stations_transmissions_plot.export(simulations, ensure_dir(path + 'stations_transmissions_plot.pdf'), schemes_markers)


def iteration_plots(path):
    schemes_markers = {
        simulator.Scheme.DCF_BASIC: dict(marker='s', linestyle=':'),
        simulator.Scheme.CRB: dict(marker='o', linestyle='--'),
        simulator.Scheme.TBRI: dict(marker='^', linestyle='-'),
    }

    stations_schemes_markers = {
        8: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-', linewidth=1.5),
            simulator.Scheme.TBRI: dict(marker='', linestyle='--', linewidth=1.5),
        },
        16: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-.', linewidth=1.5),
            simulator.Scheme.TBRI: dict(marker='', linestyle=':', linewidth=1.5),
        }
    }

    range_stations = range(8, 16 + 1, 8)
    range_iterations = [300] + list(range(3000, 300000 + 1, 3000))

    simulations = simulator.run_multiple(range_iterations, schemes_markers.keys(), range_stations)

    iterations_transmissions_plot.export(simulations, ensure_dir(path + 'iterations_transmissions_plot.pdf'), schemes_markers)
    iteration_syncnodes_plot.export(simulations[15000], ensure_dir(path + 'iteration_syncnodes_plot.pdf'), stations_schemes_markers)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout, format='%(message)s')
    print(cpu_count())
    path = 'output/{}/'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    import random
    random.seed(2)

    # station_plots(path)
    iteration_plots(path)
