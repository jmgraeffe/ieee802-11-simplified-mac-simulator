import logging
import sys
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

    simulations = simulator.run_multiple(schemes_markers.keys(), range_stations, 1000000)

    station_collision_plot.export(simulations, ensure_dir(path + 'stations_collisions_plot.pdf'), schemes_markers)
    stations_transmissions_plot.export(simulations, ensure_dir(path + 'stations_transmissions_plot.pdf'), schemes_markers)


def iteration_plots(path):
    schemes_markers = {
        simulator.Scheme.DCF_BASIC: dict(marker='s', linestyle=':'),
        simulator.Scheme.CRB: dict(marker='o', linestyle='--'),
        simulator.Scheme.TBRI: dict(marker='^', linestyle='-'),
    }

    stations_schemes_markers = {
        20: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-', linewidth=0.5),
            simulator.Scheme.TBRI: dict(marker='', linestyle='--', linewidth=1.5),
        },
        30: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-.', linewidth=0.5),
            simulator.Scheme.TBRI: dict(marker='', linestyle=':', linewidth=1.5),
        }
    }

    range_stations = range(20, 30 + 1, 10)
    range_iterations = [300] + list(range(3000, 300000 + 1, 3000))

    simulations = {}
    for num_iterations in range_iterations:
        simulations[num_iterations] = simulator.run_multiple(schemes_markers.keys(), range_stations, num_iterations)

    iterations_transmissions_plot.export(simulations, ensure_dir(path + 'iterations_transmissions_plot.pdf'), schemes_markers)
    iteration_syncnodes_plot.export(simulations[300000], ensure_dir(path + 'iteration_syncnodes_plot.pdf'), stations_schemes_markers)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout, format='%(message)s')
    print(cpu_count())
    path = 'output/{}/'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    station_plots(path)
    iteration_plots(path)
