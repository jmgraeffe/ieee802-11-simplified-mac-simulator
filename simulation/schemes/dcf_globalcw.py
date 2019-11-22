import random

from .dcf_basic import Station as DcfStation, Simulator as DcfSimulator, Medium as DcfMedium


class Station(DcfStation):
    def tick(self):
        """Gets called by simulation on every time slot to determine what the current backoff is.
        """
        if self.backoff is None:
            self.backoff = random.randrange(self.medium.cw_size + 1)

        self.backoff -= 1


class Medium(DcfMedium):
    def __init__(self, cw_start, cw_end):
        super().__init__(cw_start, cw_end)
        self.cw_size = cw_start


class Simulator(DcfSimulator):
    def __init__(self, num_stations, num_iterations, cw_start, cw_end):
        super().__init__(num_stations, num_iterations, cw_start, cw_end)
        self.medium = Medium(cw_start, cw_end)
        self.stations = self.generate_stations(num_stations)

    def generate_station(self, num):
        return Station(num, self.medium)

    def do_contention_phase(self):
        collisions, sender = super().do_contention_phase()

        if collisions > 0:
            self.medium.cw_size = min(((self.medium.cw_size + 1) * 2) - 1, self.medium.cw_end)
        else:
            self.medium.cw_size = self.medium.cw_start
        print('cw_size set to {}'.format(self.medium.cw_size))

        return (collisions, sender)
