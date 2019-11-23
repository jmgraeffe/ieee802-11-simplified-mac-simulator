import random

from .. import Scheme
from .crb import Simulation as CrbSimulation, Station as CrbStation, Medium as CrbMedium, Simulator as CrbSimulator, AccessPoint as CrbAccessPoint


class AccessPoint(CrbAccessPoint):
    def _send_ack(self, station, *args):
        # don't send it directly to station, since the medium will broadcast it to everyone in 3bRI
        # also append slot reservation information
        slots = self._construct_slot_information()
        self.medium.ack(station, *args, slots)

    def _construct_slot_information(self):
        # False represents unreserved slot
        slots = [False] * 3

        for backoff_counter, station in self.synchronized_stations.items():
            # if backoff_counter == 1: first slot will be reserved
            # if backoff_counter == 3: third slot will be reserved
            # => WARNING, no first slot anomaly in this simulation!
            if backoff_counter >= 0 and backoff_counter <= 2:
                # True represents reserved slot
                slots[backoff_counter] = True

        return slots


class Station(CrbStation):
    def __init__(self, num, medium):
        super().__init__(num, medium)
        self.reserved_slots = []  # our famous 3 bits of slot reservation information after which the whole thing is named (3bRI)

    def tick(self):
        if len(self.reserved_slots) > 0:
            # virtual collisions with reservation information only for UCNs!
            if self.synchronized is False:
                if self.backoff == 0:
                    self.backoff = random.randrange(self.cw_size + 1)
                else:
                    self.backoff -= 1

                # if we're basically just before sending (UCNs will decrement backoff counter to zero in super method)
                if self.backoff == 0:
                    # if the current slot is reserved
                    if self.reserved_slots[0] is True:
                        # double contention window size
                        self.cw_size = min(((self.cw_size + 1) * 2) - 1, self.medium.cw_end)

                        # generate new backoff counter
                        self.backoff = random.randrange(self.cw_size + 1)
                    # otherwise we can try to send
                    else:
                        self.medium.send(self)
            # do the usual stuff
            else:
                super().tick()
            # we consumed the reservation information
            self.reserved_slots.pop(0)
        else:
            super().tick()

    def ack(self, intended_receiver, next_backoff, backoff_stage, slots):
        # simulate that we can't hear the first 13 bits of CRB info (would be encrypted in reality)
        if self == intended_receiver:
            # if we're the intended receiver, we can synchronize
            super().ack(next_backoff, backoff_stage)
        else:
            self.reserved_slots = slots.copy()


class Medium(CrbMedium):
    def __init__(self, cw_start, cw_end, stations):
        super().__init__(cw_start, cw_end)
        self.ap = AccessPoint(self, cw_start, cw_end)
        self.stations = None  # unrealistic, but used for getting access to stations to inform all hearing stations about the 3 bits of reservation information

    def ack(self, intended_receiver, *args):
        for station in self.stations:
            station.ack(intended_receiver, *args)


class Simulator(CrbSimulator):
    def __init__(self, num_stations, num_iterations, cw_start, cw_end):
        self.num_stations = num_stations
        self.num_iterations = num_iterations
        self.simulation = CrbSimulation(Scheme.TBRI, num_stations, num_iterations, cw_start, cw_end)
        self.medium = Medium(cw_start, cw_end, self)
        self.stations = self.generate_stations(num_stations)
        self.medium.stations = self.stations  # dirty injection

    def generate_station(self, num):
        return Station(num, self.medium)
