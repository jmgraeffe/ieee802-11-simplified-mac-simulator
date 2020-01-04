import matplotlib.pyplot as plt

from simulation import Scheme


def export(simulations, file_path, marker_styles=None):
    xticks = []

    for scheme, simulations2 in simulations.items():
        xs = []
        ys = []

        for num_stations, simulation in simulations2.items():
            if num_stations not in xticks and num_stations % 10 == 0:
                xticks.append(num_stations)

            xs.append(num_stations)
            ys.append(simulation.successful_transmissions)

        if marker_styles is None:
            plt.plot(xs, ys, 'o-', label=Scheme.to_human_name(scheme))
        else:
            plt.plot(xs, ys, label=Scheme.to_human_name(scheme), **marker_styles[scheme])

    plt.grid()
    plt.xlabel('Number of Stations')
    plt.ylabel('Number of Successful Transmissions')
    plt.xticks(xticks)
    plt.legend(fancybox=True, framealpha=1.0)
    plt.savefig(file_path, bbox_inches='tight')
    plt.clf()
