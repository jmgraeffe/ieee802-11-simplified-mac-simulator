from datetime import datetime

from common_functions import ensure_dir
import simulation as simulator
from exporters import station_collision_plot


if __name__ == '__main__':
    schemes_markers = {
        simulator.Scheme.DCF_BASIC: dict(marker='o', linestyle='-'),
        simulator.Scheme.DCF_NO_BACKOFF_MEMORY: dict(marker='^', linestyle='-'),
        simulator.Scheme.DCF_GLOBAL_CW: dict(marker='s', linestyle='-'),
        simulator.Scheme.CRB: dict(marker='H', linestyle='-')
    }

    range_stations = range(10, 50 + 1)
    simulations = simulator.run_multiple(schemes_markers.keys(), range_stations, 100)

    path = 'output/{}/'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    station_collision_plot.export(simulations, ensure_dir(path + 'station_collision_plot.pdf'), schemes_markers)
