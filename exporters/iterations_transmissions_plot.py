import matplotlib.pyplot as plt


def export(simulations, file_path, marker_styles=None):
    schemes = []
    xticks = []
    scheme_xs = {}
    scheme_ys = {}

    for num_iterations, scheme_simulations in simulations.items():
        xticks.append(num_iterations)

        for scheme, simulations in scheme_simulations.items():
            if scheme not in scheme_xs.keys():
                schemes.append(scheme)
                scheme_xs[scheme] = []
                scheme_ys[scheme] = []

            scheme_xs[scheme].append(num_iterations)
            scheme_ys[scheme].append(simulations[20].successful_transmissions)  # TODO: remove hardcoded 20, bad style :(

    for scheme in schemes:
        if marker_styles is None:
            plt.plot(scheme_xs[scheme], scheme_ys[scheme], 'o-', label='{}'.format(scheme))
        else:
            plt.plot(scheme_xs[scheme], scheme_ys[scheme], label='{}'.format(scheme), **marker_styles[scheme])

    plt.grid()
    plt.xlabel('number of iterations')
    plt.ylabel('number of successful transmissions')
    plt.xticks(xticks)
    plt.xscale('log')
    plt.legend(fancybox=False)
    plt.savefig(file_path)
    plt.clf()
