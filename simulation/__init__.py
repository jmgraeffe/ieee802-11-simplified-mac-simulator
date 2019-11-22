from enum import Enum

"""TODO
-
"""


class Scheme(Enum):
    DCF_BASIC = 1
    DCF_NO_BACKOFF_MEMORY = 2
    DCF_GLOBAL_CW = 3
    CRB = 4,
    TBRI = 5  # 3bRI, 3 bit of reservation information, three bit scheduling


def run(scheme=Scheme.DCF_BASIC, num_stations=50, num_iterations=1000, cw_start=15, cw_end=255):
    if scheme is Scheme.DCF_BASIC:
        from .schemes.dcf_basic import Simulator
    elif scheme is Scheme.DCF_NO_BACKOFF_MEMORY:
        from .schemes.dcf_nobackoffmemory import Simulator
    elif scheme is Scheme.DCF_GLOBAL_CW:
        from .schemes.dcf_globalcw import Simulator
    elif scheme is Scheme.CRB:
        from .schemes.crb import Simulator
    elif scheme is Scheme.TBRI:
        from.schemes.tbri import Simulator
    else:
        print('Scheme \'{}\' not implemented!'.format(scheme))
        return

    simulation = Simulator(num_stations, num_iterations, cw_start, cw_end).run()
    return simulation
    # print(simulation.log)


def run_multiple(schemes, range_stations, num_iterations=1000, cw_start=15, cw_end=255):
    simulations = {}

    for scheme in schemes:
        simulations[scheme] = {}

        for num_stations in range_stations:
            print('BLA')
            print(num_stations)
            simulations[scheme][num_stations] = run(scheme, num_stations, num_iterations, cw_start, cw_end)

    return simulations
