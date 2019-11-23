import matplotlib.pyplot as plt


def export(simulations, file_path, marker_styles=None):
    for scheme, num_stations_simulations in simulations.items():
        for num_stations, simulation in num_stations_simulations.items():
            if marker_styles is None or scheme in marker_styles[num_stations].keys():
                xs = []
                ys = []

                for iteration, num_synchronized_nodes in enumerate(simulation.num_synchronized_nodes):
                    xs.append(iteration)
                    ys.append(num_synchronized_nodes)

                if marker_styles is None:
                    plt.plot(xs, ys, 'o-', label='{}, {} stations'.format(scheme, num_stations))
                else:
                    plt.plot(xs, ys, label='{}, {} stations'.format(scheme, num_stations), **marker_styles[num_stations][scheme])

    plt.grid()
    plt.xlabel('iteration (time slot)')
    plt.ylabel('number of SCN\'s')
    plt.legend(fancybox=False)
    plt.savefig(file_path)
    plt.clf()