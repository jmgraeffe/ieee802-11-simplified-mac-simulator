import random
import logging

from ..classes import *
from .. import Scheme

MAXIMUM_ITERATIONS_STATION_LOG = 10000


class Station(Station):
    def __init__(self, num, medium):
        super().__init__(num, medium)
        self.cw_size = medium.cw_start
        self.backoff = 0

    def tick(self):
        """Gets called by simulation on every time slot to determine what the current backoff is.
        """
        if self.backoff == 0:
            self.backoff = random.randrange(self.cw_size + 1)
        else:
            self.backoff -= 1

        if self.backoff == 0:
            self.medium.send(self)

    def feedback(self, collision):
        """Gets called by simulation when station attempted to send data (backoff count = 0) as a feedback wether it worked or not.
        """
        # if a collision occurred, increase contention window size until cw_end is reached
        if collision is True:
            self.cw_size = min(((self.cw_size + 1) * 2) - 1, self.medium.cw_end)
        # otherwise, on successful transmission, reset contention window size
        else:
            self.cw_size = self.medium.cw_start


class Medium(Medium):
    def __init__(self, cw_start, cw_end):
        super().__init__(AccessPoint(self))
        self.cw_start = cw_start
        self.cw_end = cw_end


class Simulator:
    def __init__(self, num_stations, num_iterations, cw_start, cw_end):
        self.num_stations = num_stations
        self.num_iterations = num_iterations
        self.simulation = Simulation(Scheme.DCF_BASIC, num_stations, num_iterations, cw_start, cw_end)
        self.medium = Medium(cw_start, cw_end)
        self.stations = self.generate_stations(num_stations)

    def generate_station(self, num):
        return Station(num, self.medium)

    def generate_stations(self, num_stations):
        stations = []

        for num in range(num_stations):
            stations.append(self.generate_station(num))

        return stations

    def _iteration_output(self, frame):
        if isinstance(frame, CollisionFrame) is True:
            logging.info('collisions_stations({}) = {}'.format(self.medium.iteration, frame.collisions))
        else:
            logging.info('collisions_stations({}) = 0'.format(self.medium.iteration))

    def run(self):
        # we start with a contention phase, which is a simplification of the simulation
        for iteration in range(self.num_iterations):
            # let every station decide what to do
            for station in self.stations:
                station.tick()

            # let's see what the outcome of the medium's time slot is
            frame = self.medium.evaluate_iteration()

            # some counting for analysis
            if isinstance(frame, DataFrame) is True:
                self.simulation.successful_transmissions += 1
            elif isinstance(frame, CollisionFrame) is True:
                self.simulation.collisions_stations += frame.collisions
                self.simulation.collisions_ap += 1

            # self.simulation.frame_log.append(frame)
            # if len(self.simulation.station_log) < MAXIMUM_ITERATIONS_STATION_LOG:
            #     self.simulation.station_log.append(self.stations)
            self._iteration_output(frame)

            # clear everything up for next iteration
            self.medium.next_iteration()

        return self.simulation
