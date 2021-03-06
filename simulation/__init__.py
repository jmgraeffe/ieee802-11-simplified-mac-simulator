from enum import Enum
from multiprocessing import cpu_count, Pool
import logging
import collections
import time


class Scheme(Enum):
    DCF_BASIC = 1
    DCF_NO_BACKOFF_MEMORY = 2
    DCF_GLOBAL_CW = 3
    CRB = 4,
    TBRI = 5  # 3bRI, 3 bit of reservation information, three bit scheduling

    @classmethod
    def to_human_name(cls, scheme):
        if scheme is cls.DCF_BASIC:
            return 'DCF'
        elif scheme is cls.CRB:
            return 'CRB'
        elif scheme is cls.TBRI:
            return '3bRI'
        else:
            return str(scheme)


def run(scheme=Scheme.DCF_BASIC, num_stations=50, num_iterations=1000, cw_start=15, cw_end=255):
    if scheme is Scheme.DCF_BASIC:
        from .schemes.dcf_basic import Simulator
    # elif scheme is Scheme.DCF_NO_BACKOFF_MEMORY:
    #     from .schemes.dcf_nobackoffmemory import Simulator
    # elif scheme is Scheme.DCF_GLOBAL_CW:
    #     from .schemes.dcf_globalcw import Simulator
    elif scheme is Scheme.CRB:
        from .schemes.crb import Simulator
    elif scheme is Scheme.TBRI:
        from.schemes.tbri import Simulator
    else:
        logging.error('Scheme \'{}\' not implemented!'.format(scheme))
        return

    simulation = Simulator(num_stations, num_iterations, cw_start, cw_end).run()

    logging.info('-' * 64)
    logging.info('collisions_ap\t\t\t\t= {}'.format(simulation.collisions_ap))
    logging.info('collisions_stations\t\t\t= {}'.format(simulation.collisions_stations))
    logging.info('successful_transmissions\t= {}'.format(simulation.successful_transmissions))
    logging.info('-' * 64)

    return simulation


def run_process(args):
    return run(*args)


def run_multiple(range_iterations, schemes, range_stations, cw_start=15, cw_end=255):
    simulations = collections.OrderedDict()
    process_args = []

    for num_iterations in range_iterations:
        simulations[num_iterations] = collections.OrderedDict()

        for scheme in schemes:
            simulations[num_iterations][scheme] = collections.OrderedDict()

            for num_stations in range_stations:
                process_args.append((scheme, num_stations, num_iterations, cw_start, cw_end))

    with Pool(processes=int(3 * cpu_count() / 4)) as pool:
        results = pool.map(run_process, process_args)

    for result in results:
        simulations[result.num_iterations][result.scheme][result.num_stations] = result

    return simulations


def run_multiple_averaged(num_simulations, range_iterations, schemes, range_stations, cw_start=15, cw_end=255):
    start = time.time()
    first = run_multiple(range_iterations, schemes, range_stations, cw_start, cw_end)
    end = time.time()

    print("1. simulation finished in {} seconds!".format(end - start))

    # add statistics of all missing simulations to the first one
    for num_simulation in range(num_simulations - 1):
        start = time.time()
        simulations = run_multiple(range_iterations, schemes, range_stations, cw_start, cw_end)
        end = time.time()

        print("{}. simulation finished in {} seconds!".format(num_simulation + 2, end - start))

        for num_iterations, simulations1 in simulations.items():
            for scheme, simulations2 in simulations1.items():
                for num_stations, simulation in simulations2.items():
                    first[num_iterations][scheme][num_stations].add(simulation)

    # divide everything to get average
    for num_iterations, simulations1 in first.items():
        for scheme, simulations2 in simulations1.items():
            for num_stations, simulation in simulations2.items():
                first[num_iterations][scheme][num_stations].divide_by(num_simulations)

    return first
