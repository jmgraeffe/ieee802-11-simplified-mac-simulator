import random

from .dcf_basic import *


class Station(Station):
    def tick(self):
        """Gets called by simulation on every time slot to determine what the current backoff is.
        """
        self.backoff = random.randrange(self.cw_size + 1)


class Simulator(Simulator):
    def generate_station(self, num):
        return Station(num, self.medium)
