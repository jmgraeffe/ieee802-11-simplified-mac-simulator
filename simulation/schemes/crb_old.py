import random

from .dcf_basic import Station as DcfStation, Simulator as DcfSimulator


class AccessPoint(DcfStation):
    def __init__(self, medium, cw_start, cw_end):
        super().__init__(-1, medium)
        self.cw_start = cw_start  # W_0
        self.cw_end = cw_end  # m * W_0
        self.synchronized_stations = {}  # key "assigned backoff": value "SCN"
        self.first_iteration = None

    def calculate_cw_size(self, backoff_stage):
        return (self.cw_start + 1) * (backoff_stage + 1) - 1

    def vba(self, station):
        backoff_stage = 0

        while True:
            cw_size = self.calculate_cw_size(backoff_stage)
            backoff_counter = random.randrange(cw_size + 1)

            if self.first_iteration is None:
                self.first_iteration = self.medium.iteration

            # old: relative_backoff = (backoff_counter - (self.medium.iteration - self.first_iteration)) % (cw_size + 1)
            relative_backoff = abs((cw_size - backoff_counter - self.medium.iteration + self.first_iteration) % (cw_size + 1) - cw_size)

            if relative_backoff not in self.synchronized_stations.keys():
                # the given station now gets synchronized by the AP ...
                self.synchronized_stations[relative_backoff] = station

                # ... and therefore get his own backoff assigned by Virtual Backoff Algorithm
                # old: timed_backoff = (self.medium.iteration - self.last_iteration) % self.cw_size + backoff
                station.synchronize(backoff_counter, backoff_stage, relative_backoff)
                break
            else:
                # double the contention window (increase backoff stage) due to virtual collision
                if cw_size < self.cw_end:
                    backoff_stage += 1
                    print('backoff_stage set to {}'.format(backoff_stage + 1))


class Station(DcfStation):
    synchronized = False  # SCN if True, UCN if False
    next_backoff = None  # TODO does node lose aquired backoff after sucessfully sending one data frame?
    backoff_stage = None
    relative_backoff = None  # only for analysis

    def tick(self):
        """Gets called by simulation on every time slot to determine what the current backoff is.
        """
        if self.backoff is None:
            if self.synchronized is True:
                # the AP just gave us a backoff count to use
                if self.next_backoff is not None:
                    self.backoff = self.next_backoff
                    self.next_backoff = None
                # otherwise, we need wait full time again
                # TODO is this really how it works?
                else:
                    self.backoff = self.medium.ap.calculate_cw_size(self.backoff_stage)
            else:
                self.backoff = random.randrange(self.cw_size + 1)
        else:
            self.backoff -= 1

    def synchronize(self, next_backoff, backoff_stage, relative_backoff):
        self.synchronized = True
        self.next_backoff = next_backoff
        self.backoff_stage = backoff_stage
        self.relative_backoff = relative_backoff  # only for analysis

    def feedback(self, collision):
        """Gets called by simulation when station attempted to send data (backoff count = 0) as a feedback wether it worked or not.
        """
        super().feedback(collision)

        if collision is False and self.synchronized is False:
            # theoretically, the information which ap.vba sets is in the ACK frame - in our simulation, we just let the AP synchronize the station
            self.medium.ap.vba(self)


class Simulator(DcfSimulator):
    def __init__(self, num_stations, num_iterations, cw_start, cw_end):
        super().__init__(num_stations, num_iterations, cw_start, cw_end)
        self.medium.ap = AccessPoint(self.medium, cw_start, cw_end)  # dirty injection
        self.stations = self.generate_stations(num_stations)
        print('BLI')
        print(num_stations)

    def generate_station(self, num):
        return Station(num, self.medium)

    def do_contention_phase(self):
        print('#SCNs({}) = {}'.format(self.medium.iteration, len(self.medium.ap.synchronized_stations)))
        return super().do_contention_phase()

    def run(self):
        super().run()
        print(self.medium.ap.synchronized_stations.keys())
        return self.simulation
