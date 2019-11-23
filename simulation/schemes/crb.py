import math
import random
import logging

from ..classes import AccessPoint as AP, Simulation as OldSimulation
from .dcf_basic import Station as DcfStation, Medium as DcfMedium, Simulator as DcfSimulator


class AccessPoint(AP):
    def __init__(self, medium, cw_start, cw_end):
        super().__init__(medium)
        self.cw_start = cw_start  # W_0
        self.cw_end = cw_end  # m * W_0
        self.synchronized_stations = {}  # key "assigned backoff": value "SCN"
        self.last_iteration = None

    def calculate_cw_size(self, backoff_stage):
        return math.pow(2, backoff_stage) * (self.cw_start + 1) - 1

    def data(self, station):
        # if not yet synchronized, we run VBA to attempt to synchronize it
        # (theoretically, the AP would look this up in his tables,
        # but for easier programming, we just take the short path)
        if station.synchronized is False:
            self._vba(station)

    def collision(self, stations):
        # unsynchronize stations which are synchronized but caused a collision just now
        for station in stations:
            if station in self.synchronized_stations.values():
                self._unsynchronize(station)

    def _update_backoffs(self, elapsed_iterations):
        new_stations = {}

        for backoff_counter, station in self.synchronized_stations.items():
            cw_size = self.calculate_cw_size(station.backoff_stage)
            new_backoff_counter = (backoff_counter - elapsed_iterations) % (cw_size + 1)
            logging.debug(backoff_counter)
            logging.debug(elapsed_iterations)
            logging.debug(cw_size)
            logging.debug(new_backoff_counter)
            logging.debug('-----')
            new_stations[int(new_backoff_counter)] = station

        self.synchronized_stations = new_stations

    def _unsynchronize(self, station):
        new_stations = {}

        for backoff_counter, scn in self.synchronized_stations.items():
            if scn != station:
                new_stations[backoff_counter] = scn

        self.synchronized_stations = new_stations

    def _send_ack(self, station, backoff_counter, backoff_stage):
        """This function is solely extracted from _vba to overwrite it in the future. That's a good reason to do it, right?
        """
        station.ack(backoff_counter, backoff_stage)

    def _vba(self, station):
        backoff_stage = 0

        if self.last_iteration is not None:
            self._update_backoffs(self.medium.iteration - self.last_iteration)

        while True:
            cw_size = self.calculate_cw_size(backoff_stage)
            backoff_counter = random.randrange(cw_size + 1)

            if backoff_counter not in self.synchronized_stations.keys():
                # the given station now gets synchronized by the AP ...
                self.synchronized_stations[backoff_counter] = station

                # ... and therefore get his own backoff assigned by Virtual Backoff Algorithm
                # old: timed_backoff = (self.medium.iteration - self.last_iteration) % self.cw_size + backoff
                self._send_ack(station, backoff_counter, backoff_stage)
                break
            else:
                # double the contention window (increase backoff stage) due to virtual collision
                if cw_size < self.cw_end:
                    backoff_stage += 1
                    logging.debug('backoff_stage set to {}'.format(backoff_stage + 1))

        self.last_iteration = self.medium.iteration
        logging.debug(self.medium.iteration)


class Station(DcfStation):
    def __init__(self, num, medium):
        super().__init__(num, medium)
        self.synchronized = False  # SCN if True, UCN if False
        self.next_backoff = None  # TODO does node lose aquired backoff after sucessfully sending one data frame?
        self.backoff_stage = None

    def tick(self):
        """Gets called by simulation on every time slot to determine what the current backoff is.
        """
        if self.synchronized is True:
            if self.backoff == 0:
                # the AP just gave us a backoff count to use
                if self.next_backoff is not None:
                    self.backoff = self.next_backoff
                    self.next_backoff = None
                # otherwise, we need wait full time again
                else:
                    self.backoff = self.medium.ap.calculate_cw_size(self.backoff_stage)
            else:
                self.backoff -= 1

            if self.backoff == 0:
                self.medium.send(self)
        else:
            super().tick()

    def ack(self, next_backoff, backoff_stage):
        self.synchronized = True
        self.next_backoff = next_backoff
        self.backoff_stage = backoff_stage

    def feedback(self, collision):
        """Gets called by simulation when station attempted to send data (backoff count = 0) as a feedback wether it worked or not.
        """
        super().feedback(collision)

        if collision is True and self.synchronized is True:
            self.synchronized = False


class Medium(DcfMedium):
    def __init__(self, cw_start, cw_end):
        super().__init__(cw_start, cw_end)
        self.ap = AccessPoint(self, cw_start, cw_end)


class Simulation(OldSimulation):
    def __init__(self):
        super().__init__()
        self.num_synchronized_nodes = []


class Simulator(DcfSimulator):
    def __init__(self, num_stations, num_iterations, cw_start, cw_end):
        self.num_stations = num_stations
        self.num_iterations = num_iterations
        self.simulation = Simulation()
        self.medium = Medium(cw_start, cw_end)
        self.stations = self.generate_stations(num_stations)

    def generate_station(self, num):
        return Station(num, self.medium)

    def _iteration_output(self, frame):
        super()._iteration_output(frame)
        self.simulation.num_synchronized_nodes.append(len(self.medium.ap.synchronized_stations))
        logging.info('#SCNs({}) = {}'.format(self.medium.iteration, len(self.medium.ap.synchronized_stations)))
