import logging
import sys
from datetime import datetime
from multiprocessing import Process, cpu_count

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
        simulator.Scheme.DCF_BASIC: dict(marker='o', linestyle='-'),
        simulator.Scheme.CRB: dict(marker='^', linestyle='-'),
        simulator.Scheme.TBRI: dict(marker='s', linestyle='-'),
    }

    range_stations = range(10, 50 + 1)
    # range_stations = range(10, 15)

    simulations = simulator.run_multiple(schemes_markers.keys(), range_stations, 1000000)

    station_collision_plot.export(simulations, ensure_dir(path + 'stations_collisions_plot.pdf'), schemes_markers)
    stations_transmissions_plot.export(simulations, ensure_dir(path + 'stations_transmissions_plot.pdf'), schemes_markers)


def iteration_plots(path):
    schemes_markers = {
        simulator.Scheme.DCF_BASIC: dict(marker='s', linestyle=':'),
        simulator.Scheme.CRB: dict(marker='o', linestyle='-'),
        simulator.Scheme.TBRI: dict(marker='^', linestyle='--'),
    }

    stations_schemes_markers = {
        20: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-'),
            simulator.Scheme.TBRI: dict(marker='', linestyle='--'),
        },
        30: {
            simulator.Scheme.CRB: dict(marker='', linestyle='-.'),
            simulator.Scheme.TBRI: dict(marker='', linestyle=':'),
        }
    }

    range_stations = range(20, 30 + 1, 10)
    simulations = {300: None, 3000: None, 30000: None, 300000: None}

    for num_iterations in simulations.keys():
        simulations[num_iterations] = simulator.run_multiple(schemes_markers.keys(), range_stations, num_iterations)

    iterations_transmissions_plot.export(simulations, ensure_dir(path + 'iterations_transmissions_plot.pdf'), schemes_markers)
    iteration_syncnodes_plot.export(simulations[300000], ensure_dir(path + 'iteration_syncnodes_plot.pdf'), stations_schemes_markers)


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout, format='%(message)s')
    print(cpu_count())
    path = 'output/{}/'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    p1 = Process(target=station_plots, args=(path,))
    p2 = Process(target=iteration_plots, args=(path,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
