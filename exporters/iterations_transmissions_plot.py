import matplotlib.pyplot as plt

from simulation import Scheme


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
            scheme_ys[scheme].append(simulations[16].successful_transmissions)  # TODO: remove hardcoded 16, bad style :(

    for scheme in schemes:
        if marker_styles is None:
            plt.plot(scheme_xs[scheme], scheme_ys[scheme], 'o-', label='{}'.format(Scheme.to_human_name(scheme)))
        else:
            plt.plot(scheme_xs[scheme], scheme_ys[scheme], label='{}'.format(Scheme.to_human_name(scheme)), **marker_styles[scheme])

    plt.grid()
    plt.xlabel('Number of Iterations')
    plt.ylabel('Number of Successful Transmissions')
    # plt.xticks(xticks)
    # plt.xscale('log')
    plt.legend(fancybox=True, framealpha=1.0)
    plt.savefig(file_path, bbox_inches='tight')
    plt.clf()
