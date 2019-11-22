from datetime import datetime

from common_functions import ensure_dir
import simulation as simulator


# to destroy the randomness, while still being random
import random
# random.seed(2)


def export_station_log_csv(scheme, simulation, file_name):
    output = [''] * (len(simulation.station_log[0]) + 1)
    print(len(simulation.station_log[0]))
    for stations in simulation.station_log:
        for station in stations:
            if scheme is simulator.Scheme.CRB:  # TODO save scheme in simulation object
                output[station.num] += '{},{},'.format(station.backoff, True if station.synchronized is True else False)
            else:
                output[station.num] += '{},'.format(station.backoff)

    with open(file_name, 'a') as file:
        for s in output:
            file.write(s + '\n')


if __name__ == '__main__':
    scheme = simulator.Scheme.DCF_BASIC
    # simulation = simulator.run(scheme, num_stations=7, cw_start=3, num_iterations=5000)
    # simulation = simulator.run(scheme, num_stations=25, cw_start=63, cw_end=63, num_iterations=5000)
    simulation = simulator.run(scheme, num_stations=12, cw_start=7, num_iterations=300000)

    print('-' * 64)
    print('collisions_ap\t\t\t\t= {}'.format(simulation.collisions_ap))
    print('collisions_stations\t\t\t= {}'.format(simulation.collisions_stations))
    print('successful_transmissions\t= {}'.format(simulation.successful_transmissions))
    print('-' * 64)

    path = 'output/{}/{}_station_log.csv'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'), scheme)
    export_station_log_csv(scheme, simulation, ensure_dir(path))
