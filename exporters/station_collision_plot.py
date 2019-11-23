import matplotlib.pyplot as plt


def export(simulations, file_path, marker_styles=None):
    xticks = []

    for scheme, simulations2 in simulations.items():
        xs = []
        ys = []

        for num_stations, simulation in simulations2.items():
            if num_stations not in xticks:
                xticks.append(num_stations)

            xs.append(num_stations)
            ys.append(simulation.collisions_ap)

        if marker_styles is None:
            plt.plot(xs, ys, 'o-', label=str(scheme))
        else:
            plt.plot(xs, ys, label=str(scheme), **marker_styles[scheme])

    plt.grid()
    plt.xlabel('number of stations')
    plt.ylabel('number of collisions on AP')
    plt.xticks(xticks)
    plt.legend(fancybox=False)
    plt.savefig(file_path)
    plt.clf()
